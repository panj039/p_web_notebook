import os
import secrets
import sys
from pathlib import Path
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import markdown2
from werkzeug.utils import secure_filename

# Add util to path for importing
sys.path.insert(0, str(Path(__file__).parent.parent))
from util.paths import get_data_dir, get_templates_dir, get_static_dir

from app.auth import login_required, handle_login, handle_logout
from app.config import ALLOWED_EXTENSIONS, SECRET_KEY, DEBUG, HOST, PORT, APP_NAME, APP_DESCRIPTION

# Use unified path management
DATA_DIR = get_data_dir()
TEMPLATES_DIR = get_templates_dir()
STATIC_DIR = get_static_dir()


def create_app() -> Flask:
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder=str(TEMPLATES_DIR),
                static_folder=str(STATIC_DIR))
    
    app.secret_key = SECRET_KEY or secrets.token_hex(32)
    app.config['DEBUG'] = DEBUG

    # Make app configuration available to all templates
    @app.context_processor
    def inject_app_config():
        return {
            'APP_NAME': APP_NAME,
            'APP_DESCRIPTION': APP_DESCRIPTION
        }

    def get_file_tree(directory: Path, base_path: str = "") -> list[dict]:
        """Get file tree structure"""
        items = []
        try:
            for item in sorted(directory.iterdir()):
                if item.is_file() and item.suffix.lower() in ALLOWED_EXTENSIONS:
                    items.append({
                        'type': 'file',
                        'name': item.name,
                        'path': os.path.join(base_path, item.name).replace('\\', '/'),
                        'size': item.stat().st_size
                    })
                elif item.is_dir() and not item.name.startswith('.'):
                    items.append({
                        'type': 'directory',
                        'name': item.name,
                        'path': os.path.join(base_path, item.name).replace('\\', '/'),
                        'children': get_file_tree(item, os.path.join(base_path, item.name))
                    })
        except PermissionError:
            pass
        return items

    def search_files(query: str) -> list[dict]:
        """Search files by content and filename"""
        results = []
        query_lower = query.lower()
        
        def search_directory(directory: Path, base_path: str = ""):
            for item in directory.iterdir():
                if item.is_file() and item.suffix.lower() in ALLOWED_EXTENSIONS:
                    file_path = os.path.join(base_path, item.name).replace('\\', '/')
                    
                    # Search by filename
                    if query_lower in item.name.lower():
                        results.append({
                            'path': file_path,
                            'name': item.name,
                            'match_type': 'filename'
                        })
                        continue
                    
                    # Search by content
                    try:
                        with open(item, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if query_lower in content.lower():
                                # Find context around the match
                                lines = content.split('\n')
                                for i, line in enumerate(lines):
                                    if query_lower in line.lower():
                                        start = max(0, i - 2)
                                        end = min(len(lines), i + 3)
                                        context = '\n'.join(lines[start:end])
                                        results.append({
                                            'path': file_path,
                                            'name': item.name,
                                            'match_type': 'content',
                                            'context': context,
                                            'line': i + 1
                                        })
                                        break
                    except (UnicodeDecodeError, PermissionError):
                        continue
                elif item.is_dir() and not item.name.startswith('.'):
                    search_directory(item, os.path.join(base_path, item.name))
        
        search_directory(DATA_DIR)
        return results

    def allowed_file(filename: str) -> bool:
        """Check if file extension is allowed"""
        return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS

    # Routes
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        return handle_login()

    @app.route('/logout')
    def logout():
        return handle_logout()

    @app.route('/')
    @login_required
    def index():
        file_tree = get_file_tree(DATA_DIR)
        return render_template('index.html', file_tree=file_tree)

    @app.route('/view/<path:filepath>')
    @login_required
    def view_file(filepath: str):
        file_path = DATA_DIR / filepath
        
        if not file_path.exists() or not file_path.is_file():
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if file_path.suffix.lower() in ['.md', '.markdown']:
                html_content = markdown2.markdown(
                    content, 
                    extras=['fenced-code-blocks', 'tables', 'code-friendly']
                )
                return render_template('viewer.html', 
                                     content=html_content, 
                                     filename=file_path.name,
                                     filepath=filepath,
                                     is_markdown=True)
            else:
                return render_template('viewer.html', 
                                     content=content, 
                                     filename=file_path.name,
                                     filepath=filepath,
                                     is_markdown=False)
        except UnicodeDecodeError:
            flash('Unable to decode file content', 'error')
            return redirect(url_for('index'))

    @app.route('/edit/<path:filepath>')
    @login_required
    def edit_file(filepath: str):
        file_path = DATA_DIR / filepath
        
        if not file_path.exists() or not file_path.is_file():
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return render_template('edit.html', 
                                 content=content, 
                                 filename=file_path.name,
                                 filepath=filepath)
        except UnicodeDecodeError:
            flash('Unable to decode file content', 'error')
            return redirect(url_for('index'))

    @app.route('/save/<path:filepath>', methods=['POST'])
    @login_required
    def save_file(filepath: str):
        file_path = DATA_DIR / filepath
        content = request.form.get('content', '')
        
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            flash('File saved successfully', 'success')
        except Exception as e:
            flash(f'Error saving file: {str(e)}', 'error')
        
        return redirect(url_for('view_file', filepath=filepath))

    @app.route('/new')
    @login_required
    def new_file():
        return render_template('edit.html', content='', filename='', filepath='')

    @app.route('/create', methods=['POST'])
    @login_required
    def create_file():
        filename = request.form.get('filename', '').strip()
        content = request.form.get('content', '')
        directory = request.form.get('directory', '').strip()
        
        if not filename:
            flash('Filename is required', 'error')
            return render_template('edit.html', content=content, filename='', filepath='')
        
        # Secure the filename
        filename = secure_filename(filename)
        if not filename:
            flash('Invalid filename', 'error')
            return render_template('edit.html', content=content, filename='', filepath='')
        
        # Add extension if not present
        if not any(filename.lower().endswith(ext) for ext in ALLOWED_EXTENSIONS):
            filename += '.md'
        
        # Construct file path
        if directory:
            file_path = DATA_DIR / directory / filename
        else:
            file_path = DATA_DIR / filename
        
        if file_path.exists():
            flash('File already exists', 'error')
            return render_template('edit.html', content=content, filename=filename, filepath='')
        
        try:
            # Ensure directory exists
            file_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            flash('File created successfully', 'success')
            
            relative_path = file_path.relative_to(DATA_DIR)
            return redirect(url_for('view_file', filepath=str(relative_path).replace('\\', '/')))
        except Exception as e:
            flash(f'Error creating file: {str(e)}', 'error')
            return render_template('edit.html', content=content, filename=filename, filepath='')

    @app.route('/upload', methods=['POST'])
    @login_required
    def upload_file():
        if 'file' not in request.files:
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        file = request.files['file']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(url_for('index'))
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            directory = request.form.get('directory', '').strip()
            
            if directory:
                file_path = DATA_DIR / directory / filename
            else:
                file_path = DATA_DIR / filename
            
            try:
                # Ensure directory exists
                file_path.parent.mkdir(parents=True, exist_ok=True)
                
                file.save(file_path)
                flash('File uploaded successfully', 'success')
            except Exception as e:
                flash(f'Error uploading file: {str(e)}', 'error')
        else:
            flash('Invalid file type', 'error')
        
        return redirect(url_for('index'))

    @app.route('/search')
    @login_required
    def search():
        query = request.args.get('q', '').strip()
        results = []
        
        if query:
            results = search_files(query)
        
        return render_template('search.html', query=query, results=results)

    @app.route('/delete/<path:filepath>', methods=['POST'])
    @login_required
    def delete_file(filepath: str):
        file_path = DATA_DIR / filepath
        
        if not file_path.exists() or not file_path.is_file():
            flash('File not found', 'error')
            return redirect(url_for('index'))
        
        try:
            file_path.unlink()
            flash('File deleted successfully', 'success')
        except Exception as e:
            flash(f'Error deleting file: {str(e)}', 'error')
        
        return redirect(url_for('index'))

    # Ensure data directory exists
    DATA_DIR.mkdir(exist_ok=True)
    
    return app