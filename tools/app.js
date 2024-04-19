document.addEventListener("DOMContentLoaded", function() {
    let btSidebar = document.querySelector("#stSidebar")
    let sidebar = document.querySelector('section[data-testid="stSidebar"]')
    btSidebar?.addEventListener("click", function() {
        if(btSidebar.classList.contains("css-163ttbj")) {
            btSidebar.add("css-zp2tfc")
            btSidebar.remove("css-163ttbj")
        }else{
            btSidebar.add("css-163ttbj")
            btSidebar.remove("css-zp2tfc")
        }
    })
})