function isLoggedIn() {
    if (localStorage.hasOwnProperty("hostscanner_user_id")) {
        if (localStorage.getItem("hostscanner_user_id") != "0") {
            $(".user-email").html(localStorage.getItem("hostscanner_user_name"));
            manageMenu();
        } else {
            window.location = '/login';
        }
    } else {
        window.location = '/login';
    }
}

function logout() {
    localStorage.removeItem("hostscanner_user_id");
    localStorage.removeItem("hostscanner_user_email");
    localStorage.removeItem("hostscanner_user_status");
    window.location = '/login';
}

function setLoginSession(id, username) {
    localStorage.setItem("hostscanner_user_id", id);
    localStorage.setItem("hostscanner_user_email", username);
}

function formatDate(str) {
    var d = new Date(str);
    return d.getFullYear() + "-" + (d.getMonth() + 1 < 10 ? "0" + (d.getMonth() + 1) : d.getMonth() + 1) + "-" + d.getDate() + " " + d.getHours() + ":" + d.getDate();
}

function manageMenu() {
    var user_role = localStorage.getItem("hostscanner_user_type"),
    accordion = document.getElementById("accordion-menu");
    console.log(accordion);
    if (user_role === "Technician") {
            accordion.getElementsByTagName("li")[0].style='display:none';
            accordion.getElementsByTagName("li")[4].style='display:none';
    }

}

