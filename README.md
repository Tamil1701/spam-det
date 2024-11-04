# Spam Detection System

## Abstract
The Spam Detection System is a machine learning-powered application designed to classify messages as spam or non-spam. Utilizing a Naive Bayes classifier for reliable and efficient spam detection, this project enables users to analyze text data and determine its likelihood of being spam in real time. Built with Python and the Flask framework, the application provides a user-friendly interface that is easy to navigate, making spam detection accessible to users of all technical backgrounds. The project also includes an option to train the model with new data to continually improve accuracy, with a future goal of developing a Chrome extension for integration into email and web services.

## Features
- **Real-time Spam Detection**: Classify messages as spam or not based on model predictions.
- **Interactive Training**: Allows users to train the model with additional messages to enhance performance.
- **User-Friendly Interface**: A simple, intuitive design that’s easy to navigate for users.
- **Future Expansion**: Planned development of a Chrome extension to integrate directly into email services.

## Installation and Setup

### Prerequisites
- Ensure **Python** is installed on your system.

### Installation

1. **Clone this repository**:
   ```bash
   git clone https://github.com/Tamil1701/spam-det.git
   ```

2. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

After successfully installing the dependencies, you can start the application by running the following command:

```bash
flask run
```

Once the server starts, you can access the application through your web browser at `http://127.0.0.1:5000`.

## Usage
1. **Enter a Message**: Type or paste a message into the input field and click "Predict" to classify it as spam or not.
2. **View Result**: The system will display a message indicating if the text is likely spam or not.
3. **Train with New Data**: Use the "Train with this message" option to submit new data for the model, allowing it to improve with user input.

## Future Goals

- **Chrome Extension**: A planned browser extension will enable direct spam detection within email and web services.
- **Automated Model Updates**: Enhancements to support continuous model training with live data.
- **Multilingual Support**: Planned support for additional languages, extending usability across regions.

## Conclusion
The Spam Detection System is a versatile application developed to help users identify and manage spam effectively. With the integration of machine learning and a user-centered interface, this project aims to provide efficient spam detection and support user-driven improvements. As we continue developing the Chrome extension and exploring additional features, this application will provide even broader usability and more robust spam detection capabilities.

## References
- **Flask Documentation**: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- **scikit-learn Documentation**: [https://scikit-learn.org/](https://scikit-learn.org/)
- **Naive Bayes Classifier**: [https://en.wikipedia.org/wiki/Naive_Bayes_classifier](https://en.wikipedia.org/wiki/Naive_Bayes_classifier)
