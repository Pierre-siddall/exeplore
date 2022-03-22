function docReady(fn) {
    // see if DOM is already available
    if (document.readyState === "complete" || document.readyState === "interactive") {
        // call on next available tick
        setTimeout(fn, 1);
    } else {
        document.addEventListener("DOMContentLoaded", fn);
    }
} 

docReady(function() {
    var questions = [
        {
            question : "What was the first building to be built for the University of Exeter?",
            correct : "1",
            answer1 : "Washington Singer",
            answer2 : "Marden Hall",
            answer3 : "The Old Library",
            
        },
        {
            question : "Who opened the students' guild?",
            correct : "3",
            answer1 : "Prince Phillip",
            answer2 : "Princess Margret",
            answer3 : "Queen Elizabeth the 2nd"
        },
        {
            question : "Who opened the forum?",
            correct : "2",
            answer1 : "Prince Phillip",
            answer2 : "Queen Elizabeth the 2nd",
            answer3 : "Prince Charles"
        },
        {
            question : "How many trees are there on Exeter University's campus?",
            correct : "2",
            answer1 : "Over 1,000 trees",
            answer2 : "Over 10,000 trees",
            answer3 : "Over 100,000 trees"
        },
        {
            question : "Which British comedian came to Exeter?",
            correct : "1",
            answer1 : "Rhod Gilbert",
            answer2 : "Josh Widdicombe",
            answer3 : "Sarah Millican"
        },
        {
            question : "Which Exeter University building was used in WW2?",
            correct : "3",
            answer1 : "The Hatherley Laboratories",
            answer2 : "Northcote House",
            answer3 : "Reed Hall"
        },
        {
            question : "What is the highest point on campus?",
            correct : "2",
            answer1 : "The top of Forum Hill",
            answer2 : "The top of the physics building",
            answer3 : "Holland Hall"
        },
        {
            question : "What's the most expensive accommodation on campus?",
            correct : "1",
            answer1 : "Garden Hill House",
            answer2 : "Holland Hall",
            answer3 : "Pennsylvania Court"
        },
        {
            question : "When did the Forum open?",
            correct : "3",
            answer1 : "2000",
            answer2 : "2007",
            answer3 : "2012"
        },
        {
            question : "When was The University of Exeter founded?",
            correct : "3",
            answer1 : "1932",
            answer2 : "1947",
            answer3 : "1955"
        },
        {
            question : "Who first played at the Lemmon Grove?",
            correct : "1",
            answer1 : "Suede",
            answer2 : "Muse",
            answer3 : "Radiohead"
        },
        {
            question : "Who played at the Lemmon Grove?",
            correct : "2",
            answer1 : "The Kooks",
            answer2 : "Radiohead",
            answer3 : "Oasis"
        },
        {
            
            question : "Which Weatherspoon's used to be part of the university's campus?",
            correct : "1",
            answer1 : "The Imperial Weatherspoon's",
            answer2 : "The Chevalier Inn",
            answer3 : "George’s meeting house"
        },
        {
            
            question : "Who laid the Exeter University foundation stone?",
            correct : "2",
            answer1 : "Queen Elizabeth the 2nd",
            answer2 : "King Edward VIII",
            answer3 : "Princess Margret"
        },
        {
            
            question : "Which building was used as a wartime hospital?",
            correct : "2",
            answer1 : "Lopes",
            answer2 : "Reed Hall",
            answer3 : "Marden Hall"
        }
    ] 
    var location = document.getElementById('location');
    var answer = document.getElementById('answer');
    var option1 = document.getElementById('option1');
    var option2 = document.getElementById('option2');
    var option3 = document.getElementById('option3');
    var radio1 = document.getElementById('radio1');
    var radio2 = document.getElementById('radio2');
    var radio3 = document.getElementById('radio3');
    var form = document.getElementById('form')
    var lastResult = 0;
    //questions dictionary
    var dict = {};
    dict[1] = "one";
   
    var html5QrcodeScanner = new Html5QrcodeScanner(
        "qr-reader", { fps: 10, qrbox: 250 });
    
    function onScanSuccess(decodedText, decodedResult) {
        if (decodedText !== lastResult) {
            lastResult = decodedText;
            console.log(`Scan result = ${decodedText}`, decodedResult);
            form.hidden = false;
            location.value = `${decodedText}`;
            var q = questions[Math.floor(Math.random() * questions.length)];
            question.innerHTML = `  ${q.question}` + question.innerHTML;
            option1.innerHTML = `   ${q.answer1}` + option1.innerHTML;
            option2.innerHTML = `   ${q.answer2}` + option2.innerHTML;
            option3.innerHTML = `   ${q.answer3}` + option3.innerHTML;
            answer.value = `    ${answer}`;
            radio1.value = "1";
            radio2.value = "2";
            radio3.value = "3";

            if (q.correct == 1){
                answer.value = '1'; 
            } else if (q.correct == 2) {
                answer.value = '2';
            } else if (q.correct == 3){
                answer.value = '3';
            }

            //make the answer correct stuff work
            // also fetch question information and pass that back to the html
            
            


            html5QrcodeScanner.clear();
        }
    }
    
    // Optional callback for error, can be ignored.
    function onScanError(qrCodeError) {
        // This callback would be called in case of qr code scan error or setup error.
        // You can avoid this callback completely, as it can be very verbose in nature.
    }
    
    html5QrcodeScanner.render(onScanSuccess, onScanError);
    

    


});