class Chatbox{
    constructor(){
        this.args={
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button')
        }
        this.state=false;
        this.messages=[]; // to store message in array
        let speech=new SpeechSynthesisUtterance();
        this.sobj=speech;
        let flagS=1;
        this.flagS=flagS;// by default the speaker button is on
    }

    display(){
        const{openButton,chatBox,sendButton}=this.args;
        openButton.addEventListener('click',()=>this.toggleState(chatBox))
        sendButton.addEventListener('click',()=>this.onSendButton(chatBox))

        const node=chatBox.querySelector('input');
        node.addEventListener("keyup",({key})=>{
            if(key==='Enter'){
                this.onSendButton(chatBox);
            }
        })
    }

    toggleState(chatbox){
        this.state=!this.state;

        // show or hides the box
        if(this.state){
            chatbox.classList.add('chatbox--active')
        }
        else{
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox){
        var textField=chatbox.querySelector('input');
        let text1=textField.value;
        if(text1===""){
            return;
        }
        let msg1={name:"User",message:text1}
        this.messages.push(msg1);
        // this.messages.splice(0,0,msg1);

//         http://127.0.0.1:5000/predict
        fetch($SCRIPT_ROOT+'/predict',{
            method:'POST',
            body:JSON.stringify({message:text1}),
            mode:'cors', // cors=> cross origin resourse sharing
            headers:{
                'Content-Type':'application/json'
            },
        })
        .then(r=>r.json())
        .then(r=>{
            let msg2={name:'sam',message:r.answer};
            this.messages.push(msg2);
            // this.messages.splice(0,0,msg1);
            this.updateChatText(chatbox);
            textField.value='';
        }).catch((error)=>{
            console.error("Error:"+error);
            this.updateChatText(chatbox);
            textField.value='';
        });
    }
    updateChatText(chatbox){
        var html='';
        this.messages.slice().reverse().forEach(function(item,index){
            if(item.name=='sam')
            {
                // html+='<div class="messages__item messages__item--visitor">'+item.message+'</div>';
                html+='<div id="messages_chatbot">'+item.message+'</div>';
                // this.speakBot(item.message); // sending msg to the Speak method for speech
                let speech=new SpeechSynthesisUtterance();
                speech.text=item.message;
                let flagS=1;
                // window.alert(msg);
                if(flagS==1){
                    // window.alert("Your msg speaked");
                    window.speechSynthesis.speak(speech);
                }
            }
            else{
                // html+='<div class="messages__item messages__item--operator">'+item.message+'</div>';
                html+='<div id="messages_user">'+item.message+'</div>';

            }
        });

        const chatmessage=chatbox.querySelector('.chatbox__messages');
        chatmessage.innerHTML=html;
    }
    Sbut(){
        // window.alert('inside Sbut()');
        if(this.flagS==1){  // spaker is on, we need to off it
            document.getElementById('speaker-icon').src="static/speakerOff.jfif";
            this.flagS=0;
        }else{
            document.getElementById('speaker-icon').src="static/speakerOn.jfif";
            this.flagS=1;
        }
    }
    speakBot(msg){
        this.sobj.text=msg;
        window.alert(msg);
        if(this.flagS==1){
            window.alert("Your msg speaked");
            window.speechSynthesis.speak(this.sobj);
        }
    }
}

const chatbox=new Chatbox();
chatbox.display();

// var speakBut=document.querySelector('#speakerBut');
// var speakicon=document.querySelector('.speaker-icon');
// let flagS=1;
function SpeakerBut(){
    // // window.alert("Button clicked");
    // if(flagS==1){  // spaker is on, we need to off it
    //     document.getElementById('speaker-icon').src="static/speakerOff.jfif";
    //     flagS=0;
    // }else{
    //     document.getElementById('speaker-icon').src="static/speakerOn.jfif";
    //     flagS=1;
    // }
    // chatbox.Sbut(messages[messages.length -1])
    chatbox.Sbut()
}