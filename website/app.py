# app.py
import os
from controllers.app_controller import create_app

if __name__ == "__main__":
    app = create_app(os.path.abspath(os.path.join(os.path.dirname(__file__))))

    print(app.static_folder)
    
    app.run(debug=True)