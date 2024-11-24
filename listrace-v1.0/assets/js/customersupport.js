document.getElementById("CustomerSupport").onclick = function(){
    let email_val = document.querySelector(".subscription-input-form").value
    if(!(email_val.includes("@"))){
        window.alert("You must have an @ symbol")
    }
    else{
        document.querySelector(".appsLand-btn subscribe-btn")
    }
}