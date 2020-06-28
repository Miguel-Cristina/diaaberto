
    function formerror(name, id, type) {
    let x = document.forms["login_form"][name].value;
    console.log(x);
    if (type === "number") {
        if (x === ""  x < 0) {
            showerror(id)
        } else {
            hiddeerror(id)
        }
    } else if (type === "anoescolar") {
        if (x === ""  x <= 0 || x > 12) {
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
        }
         else {
            hiddeerror(id)
        }
    } else if (type === "email") {
        if (!RegExp('[a-z0-9._%+-]+@[a-z0-9.-]+.[a-z]{2,3}').test(x)) {
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
