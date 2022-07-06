//pull the pathname from window location
const activePage = window.location.pathname;


const navLinks = document.querySelectorAll('nav a').forEach(link => {
    if (link.href.includes(`${activePage}`)) {
        link.classList.add('active');
    }
});


if (sessionStorage.getItem('popState') != 'shown') {
    window.addEventListener("load", function () {
        setTimeout(
            function open(event) {
                document.querySelector(".popup").style.display = "block";
            },
            7000
        )
    })

}
;
document.querySelector("#close").addEventListener("click", function () {
    document.querySelector(".popup").style.display = "none";
    sessionStorage.setItem('popState', 'shown')

});

const toggleButton = document.getElementsByClassName('hamburgerMenu')[0];


toggleButton.addEventListener('click', () => {
    if (document.querySelector(".navForMobileDisplay").style.display === "none") {
        document.querySelector(".navForMobileDisplay").style.display = "";
    } else {
        document.querySelector(".navForMobileDisplay").style.display = "none";
    }

})

// document.querySelector('#outer-source__form')?.addEventListener('submit',(e)=> {
//     e.preventDefault()
//     const id = e.target.id.value
//     fetch('https://reqres.in/api/users/' + id)
//         .then(results => results.json())
//         .then(json => {
//             const image = document.querySelector('#outer-source__image1')
//             image.classList.remove('invisible')
//             image.src = json.data.avatar
//         })
//         .catch((e) => {
//         console.log(e)
//         })
// })

function myFunction(id) {

    fetch( 'https://reqres.in/api/users/'+id).then(
        response => response.json()
    ).then(
        responseOBJECT => createUsersList(responseOBJECT.data)
    ).catch(
        err => console.log(err)
    )
}

function createUsersList(response) {

    const currMain = document.querySelector("main")
      user=response
        console.log(user)
        const section = document.createElement('section')
        section.innerHTML = `
            <img src="${user.avatar}" alt="Profile Picture"/>
            <div>
             <span>${user.first_name} ${user.last_name}</span>
             <br>
             <a href="mailto:${user.email}">Send Email</a>
            </div>
        `
        currMain.appendChild(section)


}
