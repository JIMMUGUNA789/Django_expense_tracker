const usernameField = document.querySelector("#usernameField");
const feedBackArea = document.querySelector(".invalid-feedback");
const usernameSuccessOutput = document.querySelector(".usernameSuccessOutput");
const emailField = document.querySelector("#emailField");
const EmailFeedBackArea = document.querySelector(".email-invalid-feedback");
const showPasswordToggle = document.querySelector(".showPasswordToggle");
const passwordField = document.querySelector("#passwordField");
const submitBtn = document.querySelector(".submit-btn");




//username validation
// check if user has started typing and return an event
usernameField.addEventListener("keyup",(e)=>{
    console.log('user has started typing');
    // get value of user input
    const usernameVal = e.target.value;
    console.log(usernameVal);
    usernameSuccessOutput.textContent = `Checking ${usernameVal}`;

    // remove is-invalid class if no error/reset
    usernameField.classList.remove("is-invalid");
    feedBackArea.style.display='none';
    usernameSuccessOutput.style.display='block';
    // make an api call using fetch if username is not empty
    if (usernameVal.length>0){
        fetch('/authentication/validate-username/',{
            body: JSON.stringify({username: usernameVal}),
            method:"POST",
        })
        .then((res)=>res.json())
        .then(data=>{
            console.log(data);
            usernameSuccessOutput.style.display='none';
            // add class that turns field red if there's an error
            if(data.username_error){
                submitBtn.setAttribute("disabled", true)
                usernameField.classList.add("is-invalid");
                feedBackArea.style.display='block';
                feedBackArea.innerHTML=`<p>${data.username_error}</p>`;

            }else{
                submitBtn.removeAttribute("disabled");
            }
         });
    }

});


//Email validation
emailField.addEventListener("keyup", (e)=>{
    
    // get value of user input
    const emailVal = e.target.value;
    console.log(emailVal);

    // remove is-invalid class if no error/reset
    emailField.classList.remove("is-invalid");
    EmailFeedBackArea.style.display='none';
    // make an api call using fetch if username is not empty
    if (emailVal.length>0){
        fetch('/authentication/validate-email/',{
            body: JSON.stringify({email: emailVal}),
            method:"POST",
        })
        .then((res)=>res.json())
        .then(data=>{
            console.log(data);
            // add class that turns field red if there's an error
            if(data.email_error){
                submitBtn.setAttribute("disabled", true);
                emailField.classList.add("is-invalid");
                EmailFeedBackArea.style.display='block';
                EmailFeedBackArea.innerHTML=`<p>${data.email_error}</p>`;

            }else{
                submitBtn.removeAttribute("disabled");
            }
         });
    }

})

// Password Toggle
const  handleToggleInput=(e)=>{
    if(showPasswordToggle.textContent==='SHOW'){
        showPasswordToggle.textContent='HIDE';
        passwordField.setAttribute("type", "text");
    }else{
        showPasswordToggle.textContent='SHOW';
        passwordField.setAttribute("type", "password");
    }

}



showPasswordToggle.addEventListener('click', handleToggleInput);
