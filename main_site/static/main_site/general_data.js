<!-- Script for general info -->
$(document).ready (function() {
    generalInfoHandler();
});

function generalInfoHandler() {
    getGeneralData();
    loadGeneralData();
}

function getGeneralData() {
    $.ajax({
        url: '/api/general_data/',
        type: 'GET',
        'success': function(response) {
            var json = JSON.parse(response[0]);
            var cand_votes = json['cand_votes'];
            var cand_per = json['cand_per'];
            localStorage.setItem("population", json['population']);
            localStorage.setItem("inhabitants", json['inhabitants']);
            localStorage.setItem("entitled_inhabitants", json['entitled_inhabitants']);
            localStorage.setItem("distributed_ballots", json['distributed_ballots']);
            localStorage.setItem("valid_votes", json['valid_votes']);
            localStorage.setItem("votes", json['votes']);
            localStorage.setItem("cand0_per", cand_per[0]);
            localStorage.setItem("cand0_votes", cand_votes[0]);
            localStorage.setItem("cand1_per", cand_per[1]);
            localStorage.setItem("cand1_votes", cand_votes[1]);
            loadGeneralData();
        }
    })
}

function loadGeneralData() {
    document.getElementById("population").textContent = localStorage.getItem("population");
    document.getElementById("inhabitants").textContent = localStorage.getItem("inhabitants");
    document.getElementById("entitled_inhabitants").textContent = localStorage.getItem("entitled_inhabitants");
    document.getElementById("distributed_ballots").textContent = localStorage.getItem("distributed_ballots");
    document.getElementById("valid_votes").textContent = localStorage.getItem("valid_votes");
    document.getElementById("votes").textContent = localStorage.getItem("votes");
    document.getElementById("cand0_per").textContent = localStorage.getItem("cand0_per");
    document.getElementById("cand0_votes").textContent = localStorage.getItem("cand0_votes");
    document.getElementById("cand1_per").textContent = localStorage.getItem("cand1_per");
    document.getElementById("cand1_votes").textContent = localStorage.getItem("cand1_votes");
    resizeBark(document.getElementById("cand0_bark"), localStorage.getItem("cand0_per"));
    resizeBark(document.getElementById("cand1_bark"), localStorage.getItem("cand1_per"));
}
