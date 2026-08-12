const form = document.getElementById("register-form");
const message = document.getElementById("message");

form.addEventListener("submit", async (event) => {

    event.preventDefault();

    const username =
        document.getElementById("username").value;

    const email =
        document.getElementById("email").value;

    const password =
        document.getElementById("password").value;

    try {

        const response = await fetch(
            "http://localhost:8080/api/auth/register",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    username: username,
                    email: email,
                    password: password
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(
                data.message || "Registration failed"
            );
        }

        console.log("Registration response:", data);

        message.textContent = "Registration successful.";

        setTimeout(() => {
            window.location.href = "login.html";
        }, 1000);

    } catch (error) {

        console.error(error);

        message.textContent = error.message;
    }
});