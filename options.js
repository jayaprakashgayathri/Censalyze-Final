const token = localStorage.getItem("authToken");
if (!token) {
  alert("Unauthorized access. Please login first.");
  window.location.href = "login.html";
}
function logout() {
  localStorage.removeItem("authToken");
  localStorage.removeItem("username");
  window.location.reload();
}
document.addEventListener("DOMContentLoaded", function () {
  const authSection = document.getElementById("auth-section");
  const token = localStorage.getItem("authToken");
  const username = localStorage.getItem("username");

  if (token && username) {
    authSection.innerHTML = `
                <span style="margin-right: 10px;">👤 ${username}</span>
                <button class="login-button" onclick="logout()">Logout</button>
            `;
  } else {
    // Not logged in
    window.location.href = "login.html";
  }
});
