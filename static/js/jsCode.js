//pull the pathname from window location
const activePage = window.location.pathname;


const navLinks = document.querySelectorAll('nav a').forEach(link => {    
  if(link.href.includes(`${activePage}`)){
    link.classList.add('active');
  }
});




if(sessionStorage.getItem('popState') != 'shown'){
window.addEventListener("load", function(){
    setTimeout(
        function open(event){
            document.querySelector(".popup").style.display = "block";
        },
        7000
    )
})

}
;
document.querySelector("#close").addEventListener("click", function(){
    document.querySelector(".popup").style.display = "none";
    sessionStorage.setItem('popState','shown')

});

const toggleButton=document.getElementsByClassName('hamburgerMenu')[0];


toggleButton.addEventListener('click',() => {
  if (document.querySelector(".navForMobileDisplay").style.display === "none") {
    document.querySelector(".navForMobileDisplay").style.display= "";
  } else {
    document.querySelector(".navForMobileDisplay").style.display = "none";
  }

})


