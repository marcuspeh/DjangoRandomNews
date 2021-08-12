document.addEventListener('DOMContentLoaded', function() {
    if (document.querySelector("#allPost")) {
        document.querySelector("#randomNews").addEventListener("click", generateNews);
        document.querySelector('#newNewsCloseBottom').addEventListener("click", resetNews);
        document.querySelector('#newNewsCloseTop').addEventListener("click", resetNews);
        document.querySelectorAll('.deleteNews').forEach((e) => {
            e.addEventListener("click", () => deleteHistory(e.getAttribute("data-id")));
        })
    }
});



function generateNews(e) {
    // Get model components
    modalTitle = document.querySelector("#newNewsLabel");
    modalBody = document.querySelector("#newNewsBody");
    allPost = document.querySelector('#allPost');

    // Get form data
    category = document.querySelector("#category").value;

    form = new FormData();
    form.append("category", category);
    fetch("/getnews", {
        method: "POST",
        body: form,
    })
    .then((res) => res.json())
    .then((res) => {
        if (res.status == 201) {
            modalTitle.textContent = res.title;
            modalBody.innerHTML = `<img class="card-img-top" src=${res.image} alt="News Image">` +
                    `<small>By ${res.author} at ${res.date}</small>` +
                    `<p class="card-text">${res.description}</p>` +
                    `<small><a href=${res.url} target="blank">Read more...</a></small> `;
            if (document.querySelector("#noNewMessage")) {
                allPost.innerHTML = 
                `<div class="align-middle mb-2" id="post${res.id}">` +
                `<div class="card" style="width: 100%;">` +
                `<img class="card-img-top" src=${res.image} alt="News Image">` +
                `<div class="card-body">` +
                `<small>By ${res.author} at ${res.date}</small>` +
                `<h5 class="card-title">${res.title}</h5>` +
                `<p class="card-text">${res.description}</p>` +
                `<small><a href=${res.url} target="blank">Read more...</a></small>` +
                `<button class="btn btn-outline-warning deleteNews" id="delete${res.id}" style="float: right;" data-id=${res.id}>` +
                `<i class="fas fa-trash"></i></button>` +
                `</div></div></div>`
            } else {
                allPost.innerHTML = 
                `<div class="align-middle mb-2" id="post${res.id}">` +
                `<div class="card" style="width: 100%;">` +
                `<img class="card-img-top" src=${res.image} alt="News Image">` +
                `<div class="card-body">` +
                `<small>By ${res.author} at ${res.date}</small>` +
                `<h5 class="card-title">${res.title}</h5>` +
                `<p class="card-text">${res.description}</p>` +
                `<small><a href=${res.url} target="blank">Read more...</a></small>` +
                `<button class="btn btn-outline-warning deleteNews" id="delete${res.id}" style="float: right;" data-id=${res.id}>` +
                `<i class="fas fa-trash"></i></button>` +
                `</div></div></div>` +
                allPost.innerHTML;
            }
            document.querySelectorAll('.deleteNews').forEach((e) => {
                e.addEventListener("click", () => deleteHistory(e.getAttribute("data-id")));
            })
        } else {
            modalBody.innerHTML = "<p>Ops we can't find any news. Please try again.</p>"
        }
    });
};

function resetNews(e) {
    // Get model components
    modalTitle = document.querySelector("#newNewsLabel");
    modalBody = document.querySelector("#newNewsBody");
    
    // Reset modal upon closing
    modalTitle.textContent = "Random News";
    modalBody.innerHTML = '<div class="spinner-border" role="status"><span class="sr-only">Loading...</span></div>';

}

function deleteHistory(historyID) {
    // Hide news first
    history = document.getElementById(`post${historyID}`).style.display = "none";

    // Post request
    form = new FormData();
    form.append("id", historyID);
    fetch("/deletenews", {
        method: "POST",
        body: form,
    })
    .then((res) => res.json())
    .then((res) => {
        if (res.status == 201) {
        } else {
            alert("Unable to delete. Please refresh page.");
        }
    });
}