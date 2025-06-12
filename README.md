# AI Crypto Day Trading Bot

## Setup

1. Create and activate a Python virtual environment (optional but recommended):

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate


2. Install dependencies:
pip install -r requirements.txt

3. Prepare .env file:
Copy .env.example to .env

Fill in your Alpaca API keys

4. Train the model:
python train_model.py

5. Run the bot:
python crypto_trading_bot.py



Docker
Build and run with Docker:
docker build -t crypto-bot .
docker run --env-file .env crypto-bot



AWS EC2 Deployment (Summary)
Launch EC2 t2.micro instance (Amazon Linux 2)

SSH in and install Docker

Clone your repo

Build and run Docker container

Keep running with docker run -d

For detailed AWS steps, check AWS documentation or ask me.

Notes
Start with paper trading or small amounts

Monitor logs regularly

Improve model with more data and features


---

# Final Tips

- Take your time with uploads and setup  
- Ask me anytime if you get stuck or want me to help with any code or commands  
- Once comfortable, you can explore adding Telegram alerts, Twitter sentiment, or more advanced strategies

---

If you want, I can also help prepare the files as downloadable text here or help you create Git commands to upload all files easily.

---

Ready to start uploading?
