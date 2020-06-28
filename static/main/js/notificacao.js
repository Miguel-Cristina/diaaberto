function confirmacao_notificacao(id) {
    if (id === "confirmacao") {
        document.getElementById('popup_notificacao').style.display = ''
    } else if (id === "popup_cancel") {
        document.getElementById('popup_notificacao').style.display = 'none'
    }
}

console.log("javascript")
function incremental(type, id) {
    let value = document.getElementById(id).getAttribute('value')
    if (type === 'add') {
        document.getElementById(id).stepUp(1)
    } else if (type === 'minus') {
        document.getElementById(id).stepDown(1)
    }
    document.getElementById(id).setAttribute('value', value)
}

function validateForm(this_id) {
    let errormsg1 = '<div id="message_container" class="notices is-bottom">\n' +
        '    <div role="alert" class="toast is-danger is-bottom" style="">\n' +
        '        <div id="msg_here">'
    let errormsg2 = '</div>\n' +
        '    </div>\n' +
        '</div>'

    let msgdiv = document.getElementById('msgdiv')
    let assunto = document.forms["notificacao_form"]["assunto"].value;
    let conteudo = document.forms["notificacao_form"]["conteudo"].value;
    let prioridade = document.forms["notificacao_form"]["prioridade"].value;
    let utilizadortipo = document.forms["notificacao_form"]["utilizadortipo"].value;
    let tiponotificacao = document.forms["notificacao_form"]["Tiponotificacao"].value;
    let x = document.forms["notificacao_form"]["email_final"].value;
    let mail = document.forms["notificacao_form"]["utilizador_rec"].value;
    console.log(tiponotificacao)
    let y=1;
    for(let i=1; i<=x;i++){
        let k = document.forms["notificacao_form"]["id_"+i].value;
        console.log(k);
        if(k===mail){
            y=0;
        }
    }
    console.log(y);
    if (tiponotificacao === ""){msgdiv.innerHTML = errormsg1 + 'Deve escolher o tipo de notificação' + errormsg2}
    else if (y===1 && tiponotificacao === "Individual") {
        msgdiv.innerHTML = errormsg1 + 'O Utilizador não existe' + errormsg2
    } else if (tiponotificacao === "Grupo" && utilizadortipo === "escolher"){
     msgdiv.innerHTML = errormsg1 + 'Deve escolher um grupo' + errormsg2
    } else if(assunto === "" || RegExp('^[ ]+$').test(assunto) ){
       msgdiv.innerHTML = errormsg1 + 'Deve preencher o assunto' + errormsg2
    } else if(conteudo === "" || RegExp('^[ ]+$').test(conteudo) ){
       msgdiv.innerHTML = errormsg1 + 'Deve preencher o conteudo' + errormsg2
    }else if(prioridade === "" || RegExp('^[ ]+$').test(prioridade) || !RegExp('^[0-9]+$').test(prioridade)  ){
       msgdiv.innerHTML = errormsg1 + 'Deve preencher a prioridade' + errormsg2
    }
    else {
        document.getElementById('popup_notificacao').style.display=''
    }
    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);

}

function validate_editarForm(this_id) {
    let errormsg1 = '<div id="message_container" class="notices is-bottom">\n' +
        '    <div role="alert" class="toast is-danger is-bottom" style="">\n' +
        '        <div id="msg_here">'
    let errormsg2 = '</div>\n' +
        '    </div>\n' +
        '</div>'

    let msgdiv = document.getElementById('msgdiv')
    let assunto = document.forms["editar_notificacao_form"]["assunto"].value;
    let conteudo = document.forms["editar_notificacao_form"]["conteudo"].value;
    let prioridade = document.forms["editar_notificacao_form"]["prioridade"].value;
    console.log(assunto)
    if(assunto === "" || RegExp('^[ ]+$').test(assunto) ){
       msgdiv.innerHTML = errormsg1 + 'Deve preencher o assunto' + errormsg2
    } else if(conteudo === "" || RegExp('^[ ]+$').test(conteudo) ){
       msgdiv.innerHTML = errormsg1 + 'Deve preencher o conteudo' + errormsg2
    }else if(prioridade === "" || RegExp('^[ ]+$').test(prioridade) || !RegExp('^[0-9]+$').test(prioridade)  ){
       msgdiv.innerHTML = errormsg1 + 'Deve preencher a prioridade' + errormsg2
    }
    else {
        document.getElementById('popup_notificacao').style.display=''
    }
    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);

}

