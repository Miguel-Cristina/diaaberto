function validateForm(this_id, participante) {
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


    let area = document.forms["inscricao_form"]["area_estudos"].value;
    let ano = document.forms["inscricao_form"]["ano_estudos"].value;
    let p
    let alunos
    let professores
    let file
    if (participante === 'Participante Individual') {
        p = document.forms["inscricao_form"]["acompanhantes"].value;
        file = document.forms["inscricao_form"]["myfile"].value;
    } else if (participante === 'Participante em Grupo') {
        p = document.forms["inscricao_form"]["turma"].value;
        alunos = document.forms["inscricao_form"]["total_participantes"].value;
        professores = document.forms["inscricao_form"]["total_professores"].value;
    }

    let nome
    let morada
    let codigo_postal
    let localidade
    let contacto
    let escola = document.forms["inscricao_form"]["Escola"].value;
    if (escola === "others") {
        nome = document.forms["inscricao_form"]["nome"].value.toLowerCase();
        nome = nome.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
        morada = document.forms["inscricao_form"]["morada"].value;
        codigo_postal = document.forms["inscricao_form"]["codigo_postal"].value;
        localidade = document.forms["inscricao_form"]["localidade"].value;
        contacto = document.forms["inscricao_form"]["contacto"].value;
    }
    let x = document.getElementById("Escola");
    let todasescolas = ""
    let i;
    for (i = 0; i < x.length; i++) {
        todasescolas = todasescolas + "\n" + x.options[i].text;
    }
    todasescolas = todasescolas.normalize('NFD').replace(/[\u0300-\u036f]/g, "")
    let radio_refeicao = document.forms["inscricao_form"]["QuerRefeicao"].value;
    let refAlunos;
    let refOutros;
    if (radio_refeicao === '') {
        radio_refeicao = "null"
    } else if (radio_refeicao === "sim") {
        refAlunos = document.forms["inscricao_form"]["numero_aluno_normal"].value;
        refOutros = document.forms["inscricao_form"]["numero_outro_normal"].value;
    }
    let tipoTransporte = document.forms["inscricao_form"]["tipo_transporte"].value;
    let transporteEstacao;
    let qualcampus;
    if (tipoTransporte === "autocarro" || tipoTransporte === "comboio") {
        transporteEstacao = document.forms["inscricao_form"]["QuerTransportePara"].value;
        if (transporteEstacao === "sim") {
            qualcampus = document.forms["inscricao_form"]["qual"].value;
        }
    }
    let horaChegada = document.forms["inscricao_form"]["timepicker-one"].value;
    let horaPartida = document.forms["inscricao_form"]["timepicker-two"].value;
    let transporteEntreValue = document.forms["inscricao_form"]["QuerTransporteEntre"].value;
    let qualcampus2;
    let horaIda;
    let horaVolta;
    if (transporteEntreValue==="ida" || transporteEntreValue==="idavolta"){
        qualcampus2 =document.forms["inscricao_form"]["transporte_campus"].value;
        if (qualcampus2!=="escolher"){
            horaIda = document.forms["inscricao_form"]["timepicker-three"].value;
            if (transporteEntreValue==="idavolta"){
                horaVolta = document.forms["inscricao_form"]["timepicker-four"].value;
            }
        }
    }
    let rowsTotal = document.forms["inscricao_form"]["row_countt"].value;
    let rowsDeleted = document.forms["inscricao_form"]["row_deletedd"].value;
    console.log(rowsTotal)
    console.log(rowsDeleted)




    if (area === "escolha") {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher a área de estudos' + errormsg2
    } else if (ano < 0 || ano > 12 || ano === '') {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher o ano de estudos adequado' + errormsg2
    } else if (participante === 'Participante em Grupo' && !RegExp("^[A-zÀ-ÿ0-9ºª ]+$").test(p)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher um turma adequada' + errormsg2
    } else if (participante === 'Participante em Grupo' && alunos <= 0) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher numero total alunos adequado' + errormsg2
    } else if (participante === 'Participante em Grupo' && professores <= 0) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher número total professores adequado' + errormsg2
    } else if (participante === 'Participante Individual' && (p < 0 || p === '')) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher nr acompanhantes adequado' + errormsg2
    } else if (participante === 'Participante Individual' && !(RegExp("[a-zA-Z0-9-_]+.pdf$").test(file) || RegExp("[a-zA-Z0-9-_]+.png$").test(file) || RegExp("[a-zA-Z0-9-_]+.PNG$").test(file))) {
        msgdiv.innerHTML = errormsg1 + 'Deve de fazer updload do PDF ou PNG de autorização' + errormsg2
    } else if (escola === "Escolher") {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher uma escola adequada' + errormsg2
    } else if (escola === "others" && !RegExp('^[A-zÀ-ÿ0-9ºª ]+$').test(nome)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher um nome de escola adequada' + errormsg2
    } else if (escola === "others" && RegExp('^[ ]+$').test(nome)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher um nome de escola adequada' + errormsg2
    } else if (escola === "others" && todasescolas.toLowerCase().includes(nome)) {
        msgdiv.innerHTML = errormsg1 + 'Escola criada já existe' + errormsg2
    } else if (escola === "others" && !RegExp('^[A-zÀ-ÿ0-9ºª ]+$').test(morada)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher uma morada da escola' + errormsg2
    } else if (escola === "others" && RegExp('^[ ]+$').test(morada)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de escolher uma morada da escola' + errormsg2
    } else if (escola === "others" && !RegExp('^[0-9]{4}-[0-9]{3}$').test(codigo_postal)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de usar um código postal valido da escola' + errormsg2
    } else if (escola === "others" && !RegExp('^[A-zÀ-ÿ0-9 ]+$').test(localidade)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de usar uma localidade válida da escola' + errormsg2
    } else if (escola === "others" && RegExp('^[ ]+$').test(localidade)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de usar uma localidade valida da escola' + errormsg2
    } else if (escola === "others" && !RegExp('^[0-9]{9}$').test(contacto)) {
        msgdiv.innerHTML = errormsg1 + 'Deve de usar um contacto valido da escola' + errormsg2
    } else if (radio_refeicao === "null") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar se requer refeição' + errormsg2
    } else if (radio_refeicao === "sim" && (refAlunos <= 0 || refOutros <= 0)) {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar o número de refeições correto' + errormsg2
    } else if (tipoTransporte === "escolher") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar o tipo transporte que irá usar' + errormsg2
    }else if ((tipoTransporte === "autocarro" || tipoTransporte === "comboio") && transporteEstacao === "sim" && qualcampus==="escolher") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar para que campos necessita de transporte desde a estação' + errormsg2
    }else if (horaChegada===horaPartida) {
        msgdiv.innerHTML = errormsg1 + 'Hora de chegada e de partida não podem coincidir' + errormsg2
    }else if (horaChegada>=horaPartida) {
        msgdiv.innerHTML = errormsg1 + 'Hora de chegada e de partida incoerentes' + errormsg2
    }else if (horaChegada==="00 : 00") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de chegada correta' + errormsg2
    }else if (horaPartida==="00 : 00") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de partida correta' + errormsg2
    }else if (transporteEntreValue!=="nao" && qualcampus2==="escolher") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar de qual para qual campus necessita de transporte' + errormsg2
    }else if (transporteEntreValue==="ida" && qualcampus2!=="escolher" && horaIda==="00 : 00") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de ida correta' + errormsg2
    }else if (transporteEntreValue==="idavolta" && qualcampus2!=="escolher" && horaIda===horaVolta) {
        msgdiv.innerHTML = errormsg1 + 'Hora de ida e de volta não podem coincidir' + errormsg2
    }else if (transporteEntreValue==="idavolta" && qualcampus2!=="escolher" && horaIda>=horaVolta) {
        msgdiv.innerHTML = errormsg1 + 'Hora de ida e de volta incoerentes' + errormsg2
    }else if (transporteEntreValue==="idavolta" && qualcampus2!=="escolher" && horaIda==="00 : 00") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de ida correta' + errormsg2
    }else if (transporteEntreValue==="idavolta" && qualcampus2!=="escolher" && horaVolta==="00 : 00") {
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a hora de ida correta' + errormsg2
    }else if (rowsTotal==='' || rowsTotal<=0 || rowsTotal===rowsDeleted) {
        msgdiv.innerHTML = errormsg1 + 'Deve inscrever-se numa atividade' + errormsg2
    }else {
        pagination(this_id)
    }

    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);
}


function formerror(name, id, type) {
    let x = document.forms["inscricao_form"][name].value;
    console.log(x);
    if (type === "number") {
        if (x === "" || x < 0) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "anoescolar") {
        if (x === "" || x <= 0 || x > 12) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "text") {
        if (!RegExp('^[A-zÀ-ÿ ]+$').test(x)) {
            showerror(id)
        } else if (RegExp('^[ ]+$').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "mixed") {
        if (!RegExp('^[A-zÀ-ÿ0-9ºª ]+$').test(x)) {
            showerror(id)
        } else if (RegExp('^[ ]+$').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "postalcode") {
        if (!RegExp('^[0-9]{4}-[0-9]{3}$').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "movel") {
        if (!RegExp('^[0-9]{9}$').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "textandnumber") {
        if (!RegExp('^[A-zÀ-ÿ0-9 ]+$').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    }
    console.log(x)
}

function showerror(id) {
    document.getElementById(id + "_div").classList.add("has-icons-right")
    document.getElementById(id).classList.add("is-danger")
    document.getElementById(id + "_icon").style.display = ""
    document.getElementById(id + "_msg").style.display = ""
}

function hiddeerror(id) {
    document.getElementById(id + "_div").classList.remove("has-icons-right")
    document.getElementById(id).classList.remove("is-danger")
    document.getElementById(id + "_icon").style.display = "none"
    document.getElementById(id + "_msg").style.display = "none"
}