# 🐾 PetConnect

A comprehensive Django-based web platform that connects pet adopters with shelters and service providers. It facilitates pet adoption, service bookings, and manages the entire workflow from listing to delivery completion.

## ✨ Features

- **Pet Adoption System**: Browse, search, and adopt pets with integrated payment processing
- **Service Booking**: Book grooming, veterinary, and other pet services
- **Role-Based Access**: Separate dashboards for adopters, shelters, and admins
- **Payment Integration**: Razorpay payment gateway for secure transactions
- **Delivery Tracking**: Track adoption deliveries from start to completion
- **Real-time Notifications**: In-app notifications for adoption requests and bookings
- **Image Management**: Upload and manage pet and service images

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher
- pip (Python package installer)
- Git (for version control)

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/petconnect.git
   cd petconnect
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**
   
   Create a `.env` file in the project root with the following:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   RAZORPAY_KEY_ID=your_razorpay_key_id
   RAZORPAY_KEY_SECRET=your_razorpay_key_secret
   ```
   
   **Note:** Generate a Django secret key from [Django Secret Key Generator](https://djecrety.ir/) or use:
   ```python
   from django.core.management.utils import get_random_secret_key
   print(get_random_secret_key())
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

8. **Run development server**
   ```bash
   python manage.py runserver
   ```

9. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📦 Project Structure

```
petconnect/
├── accounts/          # User authentication & profiles
├── adoption/          # Pet adoption module
├── services/          # Service booking module
├── petconnect/        # Main project settings
├── templates/         # HTML templates
├── static/            # CSS, JS, images
├── media/             # User-uploaded files
├── requirements.txt   # Python dependencies
└── manage.py          # Django management script
```

## 🛠️ Technology Stack

- **Backend**: Django 5.2.7
- **Database**: SQLite (development)
- **Payment**: Razorpay API
- **Image Processing**: Pillow
- **Static Files**: WhiteNoise

## 📚 Documentation

- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Complete guide for deploying to GitHub and PythonAnywhere
- **[PROJECT_EXPLANATION.md](PROJECT_EXPLANATION.md)** - Detailed project documentation

## 🌐 Deployment

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md)

Quick links:
- **GitHub**: Upload your code to GitHub
- **PythonAnywhere**: Deploy your application for free

## 👥 User Roles

1. **Adopter**: Browse pets, submit adoption requests, book services
2. **Shelter**: Manage pet listings, handle adoption requests, offer services
3. **Admin**: Full system access and management

## 🔐 Environment Variables

Required environment variables (in `.env` file):

- `SECRET_KEY` - Django secret key (required)
- `DEBUG` - Debug mode (True/False)
- `RAZORPAY_KEY_ID` - Razorpay API key ID (optional, if using payments)
- `RAZORPAY_KEY_SECRET` - Razorpay API secret (optional, if using payments)
- `PYTHONANYWHERE_USERNAME` - Your PythonAnywhere username (for deployment)

## 📝 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues or questions, please open an issue on GitHub.

---

**Happy coding! 🎉**

