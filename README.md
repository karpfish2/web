# karpPaste_random

A simple website for creating and viewing random text pastes, optimized for the Tor network.

## Functionality

- Create new pastes (max 1 million characters)
- View random pastes without repeats
- Reset view history
- Responsive design with yellow theme
- Animations and modern interface
- Optimized for Tor network

## Installation

1. Ensure Python 3.7+ is installed  
2. Create and activate virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   # or
   .\venv\Scripts\activate  # For Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running with Tor

1. Install and configure Tor:
   ```bash
   sudo pacman -S tor
   sudo systemctl start tor
   ```

2. Configure Tor for the application:
   ```bash
   sudo nano /etc/tor/torrc
   ```
   Add these lines:
   ```
   HiddenServiceDir /var/lib/tor/karpPaste_random
   HiddenServicePort 80 127.0.0.1:5000
   ```

3. Restart Tor:
   ```bash
   sudo systemctl restart tor
   ```

4. Get your .onion address:
   ```bash
   sudo cat /var/lib/tor/karpPaste_random/hostname
   ```

5. Run the application:
   ```bash
   python run.py
   ```

## Security

- All connections secured through Tor
- Strict security headers enabled
- External dependencies disabled
- System fonts used
- Rate limiting implemented to prevent spam
- No unnecessary user data retention

## Technical Details

- Backend: Flask + SQLAlchemy
- Database: SQLite
- Frontend: HTML, CSS
- View history storage: localStorage
- Tor optimization: External dependencies disabled, system fonts, strict security headers
