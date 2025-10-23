# VibeCode Cup 2025

A Flask web app for the VibeCode Cup 2025 hackathon, hosted by AWS Cloud Club at Lovely Professional University.

## Features
- Home page with event info, ticket pricing, and prizes
- Login and Register pages
- Dashboard for participants
- Team management (create, join, view teams)
- QR code integration for quick access
- Modern UI with Tailwind CSS

## Project Structure
```
VibeCodeCup/
├── app.py                # Main Flask application
├── .env                  # Environment variables
├── requirements.txt      # Python dependencies
├── README.md             # Project documentation
├── Database/             # MongoDB connection and setup
│   └── Mongo.py
├── Models/               # User model
│   └── User.py
├── Routes/               # Flask Blueprints for app routes
│   ├── Auth.py
│   ├── Cashfree.py
│   ├── Dashboard.py
│   ├── Team.py
│   └── Ticket.py
├── static/               # Static assets
│   ├── tailwind.css
│   └── css/
│       └── main.css
├── templates/            # HTML templates
│   ├── base.html
│   ├── auth/
│   │   ├── login.html
│   │   └── register.html
│   ├── dashboard/
│   │   └── index.html
│   └── team/
│       ├── create.html
│       ├── join.html
│       └── view.html
└── venv/                 # Virtual environment (not included in version control)
```

## Ticket Pricing
INR 99 per team member

## Prizes
- **Winner:** INR 1K + Goodies + .xyz domain (for each team member worth 1.5k each) + e-certificate
- **1st Runner Up:** INR 500 + Goodies + e-certificate
- **2nd Runner Up:** INR 400 + e-certificate
- **Everyone:** Certificate of Participation

## Setup
1. Clone the repository:
   ```sh
   git clone https://github.com/shashankpandey04/vibecode-cup.git
   cd vibecode-cup
   ```
2. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\\Scripts\\activate
   ```
3. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
4. Set up environment variables in `.env`:
   ```
   MONGO_URI=mongodb://localhost:27017
   SECRET_KEY=your_secret_key
   ```
5. Run the app:
   ```sh
   python app.py
   ```
6. Open [http://127.0.0.1](http://127.0.0.1) in your browser.

## Contribution
Feel free to fork this repository and submit pull requests. For major changes, please open an issue first to discuss what you would like to change.

## License
This project is licensed under the MIT License.
