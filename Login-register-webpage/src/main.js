const loginForm = document.querySelector("#login");
const createAccountForm = document.querySelector("#createAccount");
var re = /^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
var msg = getParamURL('message');
if(msg!="")
{
    if(document.querySelector("#login")){
       setFormMessage(loginForm, 'error', msg);}
}
function setFormMessage(formElement, type, message) {
    const messageElement = formElement.querySelector(".form__message");
    messageElement.textContent = message;
    messageElement.classList.remove("form__message--success", "form__message--error");
    messageElement.classList.add(`form__message--${type}`);
}
function setInputError(inputElement, message){
    inputElement.classList.add("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = message;

}
function clearInputError(inputElement){
    inputElement.classList.remove("form__input--error");
    inputElement.parentElement.querySelector(".form__input-error-message").textContent = "";
}
function getParamURL(param) {
    return decodeURIComponent((new RegExp('[?|&]' + param + '=' + '([^&;]+?)(&|#|;|$)').exec(location.search)||[,""])[1].replace(/\+/g, '%20'))||null
   }
// email validation
function validate(email)
{
    return re.test(email);
}
function checkError(form)
{
    var errors= form.querySelectorAll(".form__input");
    for (var i = 0, len = errors.length; i < len; i++) {
        if(errors[i].parentElement.querySelector(".form__input-error-message").textContent!=""){
            alert("Fields error found!");
            return true;}
    }
    return false;
}
function isEmpty(form)
{
    var errors= form.getElementsByClassName("form__input");
    for (var i = 0, len = errors.length; i < len; i++) {
        if(errors[i].value===""){
            alert("ُEmpty field found!");
            return true;}
    }
    return false;
}
function clear(form)
{
    var errors= form.getElementsByClassName("form__input");
    for (var i = 0, len = errors.length; i < len; i++) {
        errors[i].value=""
    }
}
document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".form__input").forEach(inputElement => {
        inputElement.addEventListener("blur", e => {
            if (e.target.id === "signupUsername" && e.target.value.length < 10) {
                setInputError(inputElement, "Username must be at least 10 characters in length");
            }
            if((e.target.id === "loginEmail"||e.target.id === "signupEmail")&&!(validate(e.target.value)))
            {
                setInputError(inputElement, "Enter a valid email!");
            }
            if ((e.target.id === "loginPassword"||e.target.id === "signupPass") && e.target.value.length < 8) {
                setInputError(inputElement, "Password must be at least 8 characters in length");
            }
            if (e.target.id === "signupConfirm"&&(document.querySelector('#signupPass').value!=document.querySelector('#signupConfirm').value)) {
                setInputError(inputElement, "Password dismatch!");
            }
        });
        inputElement.addEventListener("input", e => {
            clearInputError(inputElement);

        });
    });
});
function onSubmit(){
    if(checkError(loginForm)||isEmpty(loginForm))
    { console.error("Submission error");
    return false;}
    else{
        loginForm.querySelector("#loginPassword").value = CryptoJS.MD5(loginForm.querySelector("#loginPassword").value).toString();
        return true;}
}
if(document.querySelector("#createAccount")){
createAccountForm.addEventListener('submit',s=> {
    s.preventDefault();
    const request = new XMLHttpRequest();
    request.onload = () => {
    let responseObject = null;
        try {
            responseObject = JSON.parse(request.responseText);
        } catch (e) {
            console.error('Could not parse JSON!');
        }

        if (responseObject) {
            handleResponse(responseObject);
        }
    };

    if( isEmpty(createAccountForm)||checkError(createAccountForm))
    {      
        console.error("Submission error");
   }
    else{
    const hashed= CryptoJS.MD5(createAccountForm.querySelector("#signupPass").value).toString();
    const requestData = `username=${document.getElementById('signupUsername').value}&password=${hashed}&email=${document.getElementById('signupEmail').value}`;
    request.open('post', 'register.php');
    request.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    request.send(requestData);
}
});
}
function handleResponse (responseObject) {
    if (responseObject.ok) {
        alert(`${responseObject.messages}`);
        window.location.href = 'index.html';
    } else {
        setFormMessage(createAccountForm, 'error', `${responseObject.messages}`);
        clear(createAccountForm);
    }
}

