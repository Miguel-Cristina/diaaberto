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
    let nome = document.forms["register_form"]["nome"].value;
    let deficiencias1 = document.forms["register_form"]["deficiencias1"].value;
    let deficiencias2;

    if(deficiencias1===''){
        deficiencias1='null'
    }else if(deficiencias1==='sim'){
        deficiencias2=document.forms["register_form"]["deficiencias"].value;
    }

    let password_digest = document.forms["register_form"]["password_digest"].value;
    let password_conf = document.forms["register_form"]["password_conf"].value;
    let pass;
    if(password_digest!=password_conf){
        pass='dif'
    }
    if(password_digest.length<5){
        pass='null1'
    }if(password_conf.length<5){
        pass='null2'
    }


    let permitir_localizacao = document.forms["register_form"]["permitir_localizacao"].value;
    console.log(permitir_localizacao)
    if(permitir_localizacao===''){
        permitir_localizacao='null'
    }

    let utilizar_dados_pessoais = document.forms["register_form"]["utilizar_dados_pessoais"].value;
    if(utilizar_dados_pessoais===''){
        utilizar_dados_pessoais='null'
    }

    let email = document.forms["register_form"]["email"].value;
    if(email===''){
        email='null'
    }if(!RegExp('[a-z0-9._%+-]+@[a-z0-9.-]+[.][a-z]{2,3}').test(email)){
        email='null1'
    }


    let numero_telemovel = document.forms["register_form"]["numero_telemovel"].value;
    if(numero_telemovel===''){
        numero_telemovel='null'
    }if(!RegExp('^[0-9]{9}$').test(numero_telemovel)){
        numero_telemovel='null1'
    }

    let cartao_cidadao = document.forms["register_form"]["cartao_cidadao"].value;
    if(cartao_cidadao===''){
        cartao_cidadao='null'
    }
    if(!RegExp('^[0-9]{8}$').test(cartao_cidadao)){
        cartao_cidadao='null1'
    }

    let data_nascimento = document.forms["register_form"]["data_nascimento"].value;
    if(data_nascimento===''){
        data_nascimento='null'
    }

    let utilizadortipo = document.forms["register_form"]["utilizadortipo"].value;
    let unidadeorganica;
    if(utilizadortipo ==='Participante Individual' || utilizadortipo ==='Participante em Grupo'){
        unidadeorganica='null'
    }else if(utilizadortipo === "Docente" || utilizadortipo === "Colaborador" || utilizadortipo === "Coordenador" ){
        unidadeorganica=document.forms["register_form"]["unidadeorganica"].value;
    }

    let departamento;
    if(unidadeorganica==='null' || unidadeorganica==='Escola Superior de Gestão, Hotelaria e Turismo' || unidadeorganica==='Faculdade de Economia' || unidadeorganica==='Departamento de Ciências Biomédicas e Medicina'){
       departamento='null'
    }else if(unidadeorganica==='Escola Superior de Educação e Comunicação'){
        departamento=document.forms["register_form"]["departamento_esec"].value;
    }else if(unidadeorganica==='Escola Superior de Saúde'){
        departamento=document.forms["register_form"]["departamento_ess"].value;
    }else if(unidadeorganica==='Escola Superior de Engenharia'){
        departamento=document.forms["register_form"]["departamento_ese"].value;
    }else if(unidadeorganica==='Faculdade de Ciências Humanas e Sociais'){
        departamento=document.forms["register_form"]["departamento_fchs"].value;
    }else if(unidadeorganica==='Faculdade de Ciências e Tecnologia'){
        departamento=document.forms["register_form"]["departamento_fct"].value;
    }

    let x = document.forms["register_form"]["email_final"].value;
    let mail = document.forms["register_form"]["email"].value;
    console.log(x)
    let y=1;
    for(let i=1; i<=x;i++){
        let k = document.forms["register_form"]["id_"+i].value;
        console.log(k);
        if(k===mail){
            y=0;
        }
    }
    console.log(y);


    if (nome === "" || RegExp('^[ ]+$').test(nome) || !RegExp('^[A-zÀ-ÿ ]+$').test(nome)) {
        msgdiv.innerHTML = errormsg1 + 'Deve escrever um nome real' + errormsg2
    }else if(deficiencias1==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar se tem deficiências' + errormsg2
    }else if(deficiencias1==='sim' && (RegExp('^[ ]+$').test(deficiencias2) || deficiencias2==='') ){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar quais as deficiências' + errormsg2
    }else if(utilizadortipo==='Escolher'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar o tipo de utilizador' + errormsg2
    }else if(unidadeorganica==='Escolher'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a unidade organica' + errormsg2
    }else if(departamento==='Escolher'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar o departamento' + errormsg2
    }else if(permitir_localizacao==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar se permite a localizacao' + errormsg2
    }else if(utilizar_dados_pessoais==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar se permite a utilização dos seus dados pessoais' + errormsg2
    }else if(data_nascimento==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve indicar a sua data de nascimento' + errormsg2
    }else if(pass==='dif'){
        msgdiv.innerHTML = errormsg1 + 'As passwords não coicidem' + errormsg2
    }else if(pass==='null1'){
        msgdiv.innerHTML = errormsg1 + 'A password deve de ter o número de caracteres indicado' + errormsg2
    }else if(pass==='null2'){
        msgdiv.innerHTML = errormsg1 + 'A password de confirmação deve de ter o número de caracteres indicado' + errormsg2
    }else if(email==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve de escrever um email' + errormsg2
    }else if(email==='null1'){
        msgdiv.innerHTML = errormsg1 + 'Deve de escrever um email válido' + errormsg2
    }else if(y===0){
        msgdiv.innerHTML = errormsg1 + 'Este email já existe' + errormsg2
    }else if(numero_telemovel==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve de inserir um número de telemovel' + errormsg2
    }else if(numero_telemovel==='null1'){
        msgdiv.innerHTML = errormsg1 + 'Deve de inserir um número de telemóvel válido' + errormsg2
    }else if(cartao_cidadao==='null'){
        msgdiv.innerHTML = errormsg1 + 'Deve de inserir um número de cartão de cidadão' + errormsg2
    }else if(cartao_cidadao==='null1'){
        msgdiv.innerHTML = errormsg1 + 'Deve de inserir um número de cartão de cidadão válido' + errormsg2
    }
    else {
        document.getElementById('popup_confirmacao').style.display=''
    }

    var message_ele = document.getElementById("message_container");
    setTimeout(function () {
        message_ele.style.display = "none";
    }, 4000);
}


function formerror(name, id, type,) {
    let x = document.forms["register_form"][name].value;
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
    } else if (type === "email") {
        if (!RegExp('[a-z0-9._%+-]+@[a-z0-9.-]+[.][a-z]{2,3}').test(x)) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    }else if (type === "password") {
        if (x.length<5) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    }else if (type === "cartao") {
        if (!RegExp('^[0-9]{8}$').test(x)) {
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