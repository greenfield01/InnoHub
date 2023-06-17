# Import of flask packages
from App import create_app


app = create_app()

# Start of the application
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)


# app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg',
#                                    '.png', '.gif', '.flv', '.gifv', '.webm']
