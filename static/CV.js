
function return_users(){
    let id = document.getElementById("frontend").value;

    fetch('https://reqres.in/api/users/'+id).then(
        response => response.json()
    ).then(
        response_obj => put_users_inside_html(response_obj.data)
    ).catch(
        err => console.log(err)
    )
}

function put_users_inside_html(response_obj_data) {

    const p = document.querySelector("p");
    p.innerHTML = `
    <img src="${response_obj_data.avatar}" alt="Profile Picture"/><br>
    id: ${response_obj_data.id}<br>
    email: ${response_obj_data.email}<br>
    ${response_obj_data.first_name} ${response_obj_data.last_name}<br>
    url: ${response_obj_data.support}<br>
    <a href="mailto:${response_obj_data.email}">Send Email</a>
    `;

}