function toggleSidebar() {
    var sidebar = document.getElementById("sidebar");
    var openBtn = document.getElementById("openBtn");
    var closeBtn = document.getElementById("closeBtn");

    // Verifica se o menu está aberto
    if (sidebar.classList.contains("open")) {
        sidebar.classList.remove("open"); // Fecha o menu
        setTimeout(function() {
            sidebar.style.width = "0"; // Reduz a largura após a animação
            openBtn.style.display = "flex"; // Mostra o botão de abrir
            closeBtn.style.display = "none"; // Oculta o botão de fechar
        }, 500); // Ajuste o tempo para coincidir com a animação
    } else {
        sidebar.style.width = "250px"; // Abre o menu
        sidebar.classList.add("open"); // Adiciona a classe para animação
        openBtn.style.display = "none"; // Oculta o botão de abrir
        closeBtn.style.display = "flex"; // Mostra o botão de fechar
    }
}

function toggleTools() {
    var toolsMenu = document.getElementById("toolsMenu");
    if (toolsMenu.style.display === "block") {
        toolsMenu.style.display = "none";
    } else {
        toolsMenu.style.display = "block";
    }
}

function toggleTrain() {
    var trainMenu = document.getElementById("trainMenu");
    if (trainMenu.style.display === "block") {
        trainMenu.style.display = "none";
    } else {
        trainMenu.style.display = "block";
    }
}
