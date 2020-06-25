function validateForm(this_id) {
console.log(this_id)
    let errormsg1 = '<div id="message_container" class="notices is-bottom">\n' +
        '    <div role="alert" class="toast is-danger is-bottom" style="">\n' +
        '        <div id="msg_here">'
    let errormsg2 = '</div>\n' +
        '    </div>\n' +
        '</div>'

    let successmsg1 = '<div id="message_container" class="notices is-bottom">\n' +
        '    <div role="alert" class="toast is-success is-bottom" style="">\n' +
        '        <div id="msg_here">'
    let successmsg2 = '</div>\n' +
        '    </div>\n' +
        '</div>'

    let msgdiv = document.getElementById('msgdiv')

    let data_colaboracao = document.forms["criar_colab_form"]["data_colaboracao"].value;
    if(data_colaboracao===''){
        data_colaboracao='null'
    }

    let hora_inicio_colab = document.forms["criar_colab_form"]["hora_inicio_colab"].value;
    if(hora_inicio_colab===''){
        hora_inicio_colab='null'
    }

    let hora_fim_colab = document.forms["criar_colab_form"]["hora_fim_colab"].value;
    if(hora_fim_colab===''){
        hora_fim_colab='null'
    }

    let sala_de_aula = document.forms["criar_colab_form"]["sala_de_aula"].value;
    if(sala_de_aula===''){
        sala_de_aula='null'
    }

    let percurso = document.forms["criar_colab_form"]["percurso"].value;
    if(percurso===''){
        percurso='null'
    }

    if (data_colaboracao === "null") {
        msgdiv.innerHTML = errormsg1 + 'Deve escolher uma data para colaborar' + errormsg2
    }else if(hora_inicio_colab==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de inicio da colaboração' + errormsg2
    }else if(hora_fim_colab==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de fim da colaboração' + errormsg2
    }else if(percurso==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar se pretende auxiliar no percurso' + errormsg2
    }else if(sala_de_aula==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar se pretende auxiliar na sala de aula' + errormsg2
    }else {
        document.getElementById('popup_confirmacao').style.display=''
    }

    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);
}
