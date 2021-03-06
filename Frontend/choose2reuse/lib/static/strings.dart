// ignore: avoid_classes_with_only_static_members

class ReuseStrings {
  static String appName = 'Choose2Reuse';

  //button text
  static String resetReturnButtonText = 'Start a new return';
  static String scanContainerButtonText = 'Scan container QR code';
  static String scanLocationButtonText = 'Scan location QR code';
  static String loginButtonText = 'Log in';
  static String signUpButtonText = 'Sign Up';
  static String viewAllButtonText = 'View All';
  static String useCamera = 'Use Camera';
  static String submit = 'Submit';
  static String cancel = 'Cancel';
  static String yes = 'Yes';
  static String save = 'Save';
  static String changePassword = 'Change Password';
  static String logOut = 'Log Out';
  static String done = 'Done';
  static String claimReward = 'Claim Reward';

  //page titles
  static String homepageTitle = 'Dashboard';
  static String signUpPageTitle = 'Sign Up';
  static String containerListTitle = 'Container History';
  static String profilePageTitle = 'Profile';
  static String changePasswordPageTitle = 'Change Password';
  static String forgotPasswordPageTitle = 'Forgot Password';
  static String pointsPageTitle = 'My Points';
  static String badgesPageTitle = 'My Climate Champ Badges';
  static String rewardsPageTitle = 'My Reward';
  static String returnConfirmationTitle = 'Return Confirmation';
  static String containerPassPageTitle = 'Container Pass';
  static String faqPageTitle = 'Frequently Asked Questions';
  static String contactUsPageTitle = 'Contact Us';

  //field text
  static String emailField = 'Email';
  static String passwordField = 'Password';
  static String confirmPasswordField = 'Confirm Password';
  static String firstNameField = 'First Name';
  static String middleNameField = 'Middle Name (Optional)';
  static String lastNameField = 'Last Name';
  static String classYearField = 'Class Year (Optional)';
  static String phoneNumberField = 'Phone Number';
  static String enterValidationCodeField = 'Enter code here';
  static String currentPasswordField = 'Current Password';
  static String newPasswordField = 'New Password';
  static String confirmNewPasswordField = 'Confirm New Password';
  static String homepageMessage =
      'Thank you for helping to eliminate waste from single-use takeout containers!';

  //textButton text
  static String rememberPassword = 'Remember me';
  static String goToSignUpPageText = 'Need an account? Sign up here!';
  static String goToValidationPageText =
      'Have a verification code? Enter it here!';
  static String requestNewCode = 'Request a new code';
  static String forgotPassword = 'Forgot Password';
  static String sendCode = 'Send Code';

  //label text/instructions
  static String scanLocationMessage =
      'Please scan the QR code at the drop-off location. Here is a sample QR code:';
  static String scanContainerMessage =
      'Please scan the QR code on the container.';
  static String scanBeforeTimer =
      'Please scan the QR code on the container before the timer runs out:';
  static String welcomeLabel = 'Welcome!';
  static String validationInstruction =
      'Thank you for signing up for the Choose2Reuse App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.';
  static String filterBy = 'Filter By';
  static String lostOrDamagedQuestion =
      'Please provide details to report this container as lost or damaged.';
  static String lostOrDamagedTitle = 'Report a Container';
  static String lostOrDamagedPrompt = 'Enter your reasoning here';
  static String noContainers = 'No containers found.';
  static String undoLostOrDamagedQuestion =
      'Are you sure you want to undo marking this container as damaged/lost?';
  static String myPoints = 'Points';
  static String myBadges = 'Badges';
  static String returnConfirmation15PointsText =
      'Thank you for returning a container! You have earned 15 points.';
  static String returnConfirmation5PointsText =
      'Thank you for returning a container! You have earned 5 points.';
  static String appError =
      'Please update the Choose2Reuse app to the latest version in order to continue using the app.';
  static String earnedBadgeText =
      'You have also earned a Climate Champ Badge! Your reward will expire in 5 days. To use your reward, go to the Points & Rewards page.';
  static String rewardInstructions =
      'Only press this button if you are ready to show it to a cashier! The page will only be active for 5 minutes.';
  static String redeemedAt = 'Redeemed At:';
  static String freeContainer = 'This container is free!';
  static String paidContainer = 'You need to pay for this container!';
  static String contactUsMessage =
      'Have any questions or concerns about Choose2Reuse? Email us at capstonespring2021@gmail.com';

  //snackbar messages
  static String changePassSuccess = 'Password changed successfully';
  static String updateProfileSuccess = 'Information updated successfully';

  //error message
  static String timerOutErrorMessage = 'Timer has ran out.';
  static String invalidCodeErrorMessage = 'Please enter a valid code.';
  static String emptyEmailErrorMessage = 'Please enter an email address.';
  static String passMismatchErrorMessage = 'New password fields do not match.';

  //faq sections
  static String faqSectionPoints = 'Points and Rewards';
  static String faqSectionContainers = 'Containers';

  //faq questions and answer
  static String faqQuestion1 =
      'How many points do I earn when I return a container?';
  static String faqAnswer1 =
      'Returning a container within 48 hours of checking it out will reward you 15 points; otherwise, you will receive 5 points.';
  static String faqQuestion2 = 'What can I do with points?';
  static String faqAnswer2 =
      'With every 300 points you earn, you will receive a \'Climate Champ Badge.\' With this badge, you can redeem a reward at the bakery for a free sweet treat!';
  static String faqQuestion3 = 'How do I check out a container?';
  static String faqAnswer3 =
      'First, scan the QR code on a container at a check out location using the \'Check Out Container\' feature. Then, show a cashier your \'Container Pass.\'';
  static String faqQuestion4 = 'How do I return a container?';
  static String faqAnswer4 =
      'First, scan the QR code on a return location using the \'Return Container\' feature. Then, scan the QR code of the container and leave it at the return location.';
  static String faqQuestion5 =
      'How many containers may I have checked out at once?';
  static String faqAnswer5 =
      'You may have two containers checked out at once for free. Checking out more than two containers will incur a \$5 fee per container over two.';
  static String faqQuestion6 =
      'Do I own the containers that I have checked out?';
  static String faqAnswer6 =
      'No, the containers and QR codes are the property of Stonehill College. All containers must be returned in good condition. The user will incur a \$5 fee per container that is damaged, lost, or not returned by the end of each semester.';
  static String faqQuestion7 = 'May I return someone else\'s container?';
  static String faqAnswer7 =
      'Yes, you may return any containers. You will receive points for any containers you return.';
  static String faqQuestion8 = 'What locations may I drop off my containers?';
  static String faqAnswer8 =
      'You may drop off your containers at Dining Commons​, Holy Cross Center​, Library​, Ames Sports Complex​, Shields Science Center​, Duffy Academic Center​, and Martin Institute​';
}
