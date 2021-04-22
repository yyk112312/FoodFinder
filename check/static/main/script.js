
function myFunction(e){
if(e == "CM"){
    document.getElementById("id_Height_1st").style.display="none";
    document.getElementById("id_Height_2nd").style.display="none";

    document.getElementById("id_Height_1st").value="";
    document.getElementById("id_Height_2nd").value="";

    document.getElementById("id_Height").style.display="inline-block";


}else{
    document.getElementById("id_Height").style.display="none";

    document.getElementById("id_Height").value="";

    document.getElementById("id_Height_1st").style.display="inline-block";
    document.getElementById("id_Height_2nd").style.display="inline-block";
    
}
}
//We called this function with default value=CM to show only CM field when the page loads until user clicks on Feet radio button

var selectedValue = 'CM';
if(!document.getElementById('id_HeightChoice_0').checked)
    selectedValue = 'Feet';
myFunction(selectedValue)