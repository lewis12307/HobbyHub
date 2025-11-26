const tacks = document.querySelectorAll('.tack')

tacks.forEach(t =>{
    t.computedStyleMap.transform = "rotate(45deg)";
    alert("hai");
})