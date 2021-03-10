import 'package:flutter/material.dart';

// ignore: avoid_classes_with_only_static_members
class ReuseStrings {
  static String appName() {
    return 'Choose2Reuse';
  }

  //button text
  static String scanContainerButtonText() {
    return 'Scan container QR code';
  }

  static String scanLocationButtonText() {
    return 'Scan location QR code';
  }

  static String loginButtonText() {
    return 'Log in';
  }

  static String signUpButtonText() {
    return 'Sign Up';
  }

  static String useCamera() {
    return 'Use Camera';
  }

  static String submit() {
    return 'Submit';
  }

  static String cancel() {
    return 'Cancel';
  }

  //page titles
  static String homepageTitle() {
    return 'Dashboard';
  }

  static String signUpPageTitle() {
    return 'Sign Up';
  }

  //field text
  static String emailField() {
    return 'Email';
  }

  static String passwordField() {
    return 'Password';
  }

  static String confirmPasswordField() {
    return 'Confirm Password';
  }

  static String firstNameField() {
    return 'First Name';
  }

  static String middleNameField() {
    return 'Middle Name';
  }

  static String lastNameField() {
    return 'Last Name';
  }

  static String classYearField() {
    return 'Class Year';
  }

  static String phoneNumberField() {
    return 'Phone Number';
  }

  static String enterValidationCodeField() {
    return 'Enter code here';
  }

  //textButton text
  static String rememberPassword() {
    return 'Remember me';
  }

  static String goToSignUpPageText() {
    return 'Need an account? Sign up here!';
  }

  static String goToValidationPageText() {
    return 'Have a verification code? Enter it here!';
  }

  static String requestNewCode() {
    return 'Request a new code';
  }

  //label text/instructions
  static String scanLocationMessage() {
    return 'Please scan the QR code at the drop-off location. Here is a sample QR code:';
  }

  static String scanContainerMessage() {
    return 'Please scan the QR code on the container.';
  }

  static String scanBeforeTimer() {
    return 'Please scan the QR code on the container before the timer runs out:';
  }

  static String welcomeLabel() {
    return 'Welcome!';
  }

  static String validationInstruction() {
    return 'Thank you for signing up for the Choose 2 Reuse App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.';
  }

  //error message
  static String timerOutErrorMessage() {
    return 'Timer has ran out.';
  }

  static String invalidCodeErrorMessage() {
    return 'Please enter a valid code.';
  }
}
