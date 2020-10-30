const form = document.getElementById('form');
const email = document.getElementById('email');
const password = document.getElementById('password');
const repassword = document.getElementById('repassword');
const username = document.getElementById('username');
const err_password = document.getElementById('err_password');
const err_repassword = document.getElementById('err_repassword');
const err_username = document.getElementById('err_username');
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
    if (repassword.value == '')
    {
		err_repassword.style.color = "red";
		err_repassword.innerHTML = "You must provide a paasword (Again)";
		repassword.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_repassword.style.color = "";
		err_repassword.innerHTML = "";
		repassword.style.borderColor = "";
    }
    if (username.value == '')
    {
		err_username.style.color = "red";
		err_username.innerHTML = "You must provide a Name";
		username.style.borderColor = "red";
		e.preventDefault();

    }
    else
    {
		err_username.style.color = "";
		err_username.innerHTML = "";
		username.style.borderColor = "";
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

	if (password.value.length < 6 )
	{
		err_password.innerHTML = "Passwords must be 6 charecters or longer";
		err_password.style.color = "red";
		password.style.borderColor = "red";
		e.preventDefault();

	}

	if (password.value.length > 30 )
	{
		err_password.innerHTML = "Passwords must be less than 30 charecters";
		err_password.style.color = "red";
		password.style.borderColor = "red";
		e.preventDefault();

	}


	if (email.value.length > 40 )
	{
		err_email.innerHTML = "E-mail must be less than 40 charecters";
		err_email.style.color = "red";
		email.style.borderColor = "red";
		e.preventDefault();

	}

	if (username.value.length > 25 )
	{
		err_username.innerHTML = "Name must be less than 25 charecters";
		err_username.style.color = "red";
		username.style.borderColor = "red";
		e.preventDefault();

	}

	// validate stage tow check if password doesn't match
	if (repassword.value != password.value)
	{
		err_repassword.innerHTML = "Passwords Doesn't Match";
		err_repassword.style.color = "red";
		repassword.style.borderColor = "red";
		e.preventDefault();
	}

	else
	{
		err_repassword.innerHTML = "";
		err_repassword.style.color = "";
		repassword.style.borderColor = "";
	}

		// validate stage tow check if password doesn't match
	if (username.value.match(/\d/))
	{
		err_username.innerHTML = "Name must not countain Numbers";
		err_username.style.color = "red";
		username.style.borderColor = "red";
		e.preventDefault();
	}

	else
	{
		err_username.innerHTML = "";
		err_username.style.color = "";
		username.style.borderColor = "";

	}


});

// password strength func
function password_strength()
{
	if (password.value.length <= 1)
	{
		strength.innerHTML = "";
		password.style.borderColor = "";

	}
	if (password.value.length < 6 && password.value.length > 0)
	{
		strength.innerHTML = "Very Weak";
		strength.style.color = "red";
		password.style.borderColor = "red";
	}
	if (password.value.length >= 6 )
	{
		strength.innerHTML = "Good";
		strength.style.color = "gold";
		password.style.borderColor = "gold";

	}
	if (password.value.length > 8 && password.value.match(/[A-Z]/i) && password.value.match(/\d/))
	{
		strength.innerHTML = "strong";
		strength.style.color = "green";
		password.style.borderColor = "green";

	}

}