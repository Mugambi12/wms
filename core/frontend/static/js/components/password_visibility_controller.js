function togglePassword(passwordFieldId, iconId) {
  const passwordField = document.getElementById(passwordFieldId);
  const icon = document.getElementById(iconId);

  if (passwordField.type === "password") {
    passwordField.type = "text";
    icon.name = "eye-off";
  } else {
    passwordField.type = "password";
    icon.name = "eye";
  }
}
