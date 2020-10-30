const form = document.getElementById('form');
const password = document.getElementById('password');
const newpassword = document.getElementById('newpassword');
const err_password = document.getElementById('err_password');
const err_newpassword = document.getElementById('err_newpassword');
const err_email = document.getElementById('err_email');
const strength = document.getElementById('strength');

// form valdition
form.addEventListener('submit', (e) => {

	// validate stage one check if fileds are empty
    if (password.value == '')
    {
		err_password.style.color = "red";
		err_password.innerHTML = "You must provide a paasword";
		password.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_password.style.color = "";
		err_password.innerHTML = "";
		password.style.borderColor = "";
    }
    if (newpassword.value == '')
    {
		err_newpassword.style.color = "red";
		err_newpassword.innerHTML = "You must provide a paasword (Again)";
		newpassword.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_newpassword.style.color = "";
		err_newpassword.innerHTML = "";
		newpassword.style.borderColor = "";
    }

    if (email.value == '')
    {
		err_email.style.color = "red";
		err_email.innerHTML = "You must provide an E-mail";
		email.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_email.style.color = "";
		err_email.innerHTML = "";
		email.style.borderColor = "";
    }

	if (newpassword.value.length < 6 )
	{
		err_newpassword.innerHTML = "password must be 6 charecters or longer";
		err_newpassword.style.color = "red";
		newpassword.style.borderColor = "red";
		e.preventDefault();

	}



});

// password strength func
function password_strength()
{
	if (newpassword.value.length <= 1)
	{
		strength.innerHTML = "";
		newpassword.style.borderColor = "";

	}
	if (newpassword.value.length < 6 && newpassword.value.length > 0)
	{
		strength.innerHTML = "Very Weak";
		strength.style.color = "red";
		newpassword.style.borderColor = "red";
	}
	if (newpassword.value.length >= 6 )
	{
		strength.innerHTML = "Good";
		strength.style.color = "gold";
		newpassword.style.borderColor = "gold";

	}
	if (newpassword.value.length > 8 && newpassword.value.match(/[A-Z]/i) && newpassword.value.match(/\d/))
	{
		strength.innerHTML = "strong";
		strength.style.color = "green";
		newpassword.style.borderColor = "green";

	}

}