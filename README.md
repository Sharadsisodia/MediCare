# MediCare - Patient-Doctor Appointment Booking System

MediCare is a Django-based web application designed to simplify the process of managing appointments between patients and doctors. It also provides a platform for doctors to share informative posts and content that patients can access.

## Features

### For Patients

- **Appointment Booking**: Book appointments with available doctors.
- **View Doctor Posts**: Access informative posts and updates shared by doctors.

### For Doctors

- **Post Management**: Upload and manage posts or content to share with patients.
- **Appointment Management**: View and manage appointments booked by patients.

### General Features

- **User Authentication**: Secure login and registration for both patients and doctors.
- **Responsive Design**: Optimized for both desktop and mobile devices.
- **Dynamic Web Pages**: Incorporates animations and effects for an interactive user experience.

## Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JavaScript (with animations and effects)
- **Database**: PostgreSQL
- **Integration**: Cloudinary

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/medicare.git
   ```

2. Navigate to the project directory:

   ```bash
   cd medicare
   ```

3. Create a virtual environment and activate it:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

4. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

5. Apply migrations:

   ```bash
   python manage.py migrate
   ```

6. Start the development server:

   ```bash
   python manage.py runserver
   ```

7. Open the application in your browser at `http://127.0.0.1:8000/`.

## Cloudinary Integration

1. **Install Required Packages**: Ensure you have `django-cloudinary-storage` installed.

   ```bash
   pip install django-cloudinary-storage
   ```

2. **Update Settings**: Add the following configurations:

   ```python
   CLOUDINARY_STORAGE = {
       'CLOUD_NAME': '<your-cloudinary-cloud-name>',
       'API_KEY': '<your-cloudinary-api-key>',
       'API_SECRET': '<your-cloudinary-api-secret>',
   }

   DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
   ```

3. **Environment Variables**: Store your `CLOUD_NAME`, `API_KEY`, and `API_SECRET` securely using a `.env` file or equivalent.

4. **Usage in Models**: Update `models.ImageField` to work seamlessly with Cloudinary:

   ```python
   profile_picture = models.ImageField(upload_to='profile_pics/')
   ```

5. **Deploy Notes**: Ensure your deployed environment allows for `.env` files or other secure methods for providing API credentials.

## Usage

- **Patients**: Register or log in to book appointments and view posts shared by doctors.
- **Doctors**: Register or log in to manage appointments and share content with patients.

## Future Enhancements

- **Payment Integration**: Allow patients to pay for appointments directly through the platform.
- **Notifications**: Add email and SMS notifications for appointment reminders.
- **Enhanced Search**: Improve the search functionality for finding doctors and posts.
- **Analytics Dashboard**: Provide analytics for doctors to view appointment trends and patient engagement.

## Contribution

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature/bug fix:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Add feature-name"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Author**: Sharad Sisodia

Feel free to reach out for suggestions or feedback!
