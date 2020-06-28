function validateForm(this_id) {
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
    let nome = document.forms["edit_user"]["nome"].value;
    let numero_telemovel = document.forms["edit_user"]["numero_telemovel"].value;
    let cartao_cidadao = document.forms["edit_user"]["cartao_cidadao"].value;
    let email = document.forms["edit_user"]["email"].value;








    console.log(nome);


    if (nome === "" || RegExp('^[ ]+$').test(nome)) {
        msgdiv.innerHTML = errormsg1 + 'Deve escrever um nome real' + errormsg2
    }
    else if (email === '' ||  !RegExp('[a-z0-9._%+-]+@[a-z0-9.-]+[.][a-z]{2,3}').test(email)){
        msgdiv.innerHTML = errormsg1 + 'Deve inserir um email correto' + errormsg2
    }
    else if (numero_telemovel === '' ||  !RegExp('^[0-9]{9}$').test(numero_telemovel)){
        msgdiv.innerHTML = errormsg1 + 'Deve inserir um nemero telemovel correto' + errormsg2
    }
    else if (cartao_cidadao === '' ||  !RegExp('^[0-9]{8}$').test(cartao_cidadao)){
        msgdiv.innerHTML = errormsg1 + 'Deve inserir um cartao de cidadao correto' + errormsg2
    }
    else {
        document.getElementById('popup_confirmacao').style.display=''
    }

    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);
}

function formerror(name, id, type) {
    let x = document.forms["edit_user"][name].value;
    console.log(x);
    if (type === "number") {
        if (x === "" && x < 0){
            showerror(id)
        }else{
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
    } else if (type === "movel") {
        if (!RegExp('^[0-9]{9}$').test(x)) {
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
    } else if (type === "textandnumber") {
        if (!RegExp('^[A-zÀ-ÿ0-9 ]+$').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "email") {
        if (!RegExp('[a-z0-9._%+-]+@[a-z0-9.-]+[.][a-z]{2,3}').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "cartao") {
        if (x.length!=8) {
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


function cancelbutton(id) {
    document.getElementById("popup_confirmacao").style.display="none"

}