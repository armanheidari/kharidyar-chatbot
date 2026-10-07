class Chatbox {
    constructor() {
        this.args = {
            openButton: document.querySelector('.chatbox__button'),
            chatBox: document.querySelector('.chatbox__support'),
            sendButton: document.querySelector('.send__button'),
            cart: document.querySelector('.cart')
        }

        this.stateChatBox = false;
        this.stateCart = false;
        this.mustToggleCart = false
        this.messages = [];

    }

    display() {
        const {openButton, chatBox, sendButton, cart} = this.args;

        openButton.addEventListener('click', () => this.toggleStateChatBox(chatBox, cart))

        sendButton.addEventListener('click', () => this.onSendButton(chatBox, cart))

        const node = chatBox.querySelector('input');
        node.addEventListener("keyup", ({key}) => {
            if (key === "Enter") {
                this.onSendButton(chatBox, cart)
            }
        })
    }

    toggleStateCart(cart) {
        this.stateCart = !this.stateCart;

        // show or hides the box
        if(this.stateCart) {
            cart.classList.add('cart--active')
        } else {
            cart.classList.remove('cart--active')
        }
    }

    toggleStateChatBox(chatbox, cart) {
        this.stateChatBox = !this.stateChatBox;

        if (this.mustToggleCart) {
            this.toggleStateCart(cart)
        }

        // show or hides the box
        if(this.stateChatBox) {
            chatbox.classList.add('chatbox--active')
        } else {
            chatbox.classList.remove('chatbox--active')
        }
    }

    onSendButton(chatbox, cart) {
        var textField = chatbox.querySelector('input');
        let text1 = textField.value
        if (text1 === "") {
            return;
        }

        // let msg1 = { name: "User", message: text1 }
        // this.messages.push(msg1);
        this.updateChatText(text1, 'user')

        let formData = new FormData();
        formData.append('message', text1);
        // formData.append('name', '');

        // console.log(formData)

        fetch('http://127.0.0.1:5050/predict', {
            method: 'POST',
            body: formData,
            'Access-Control-Allow-Origin': '*',
            mode: 'cors',
            // headers: {
            //   'Content-Type': 'application/json'
            // },
          })
          .then(r => r.json())
          .then(r => {
                if (r.status == "multiple_cart")
                {
                    this.multipleCartHandler(r.all_res, cart, textField)
                }
                else if (r.status == "message") {
                    this.showMessage(r)
                    textField.value = '' 
                }
                else if (r.status == "cart") {
                    if (this.stateCart == false) {
                        this.toggleStateCart(cart)
                        this.mustToggleCart = true
                    }
                    this.showMessage(r)
                    this.updateCartList(r)
                    this.updatePrice(r)
                    textField.value = ''
                }
                else if (r.status == "delete_cart") {
                    this.showMessage(r)
                    this.deleteCart()
                    this.toggleStateCart(cart)
                    textField.value = ''
                }
                else if (r.status == "order_complete") {
                    this.showMessage(r)
                    this.deleteCart()
                    this.toggleStateCart(cart)
                    textField.value = ''
                }
                else if (r.status == "edit_cart") {
                    this.showMessage(r)
                    this.deleteFromCart(r)
                    this.updateCartList(r)
                    this.updatePrice(r)
                    textField.value = ''
                }
                else {
                    console.log("UNKOWN")
                }

            }).catch((error) => {
                console.error('Error:', error);
                this.updateChatText("متاسفانه سرور به مشکل خورده است.", "bot")
                // this.updateChatText(chatbox)
                textField.value = ''
            });
    }

    multipleCartHandler(results, cart, textField) {
        for(let i = 0; i < results.length; i++) {
            let cr = results[i]
            if (cr.status == "message") {
                this.showMessage(cr)
                textField.value = ''
            }
            else if (cr.status == "cart") {
                if (this.stateCart == false) {
                    this.toggleStateCart(cart)
                    this.mustToggleCart = true
                }
                this.showMessage(cr)
                this.updateCartList(cr)
                this.updatePrice(cr)
                textField.value = ''
            }
        }
    }

    showMessageWebSocketMode() {
        const ws = new WebSocket("ws://localhost:5050/ws");
        ws.onmessage = function(event) {
            const message = event.data;
            if (message == "please close the ws") {
                ws.close()
            }
            else if (message == "$$$") {
                chatbox.updateChatText("", "bot")
            }
            else {
                chatbox.writeBotMessageDirectly(message);
            }
        };
        ws.onopen = function() {
            console.log("WebSocket connection opened");
            ws.send("ready");
        };
        ws.onclose = function() {
            console.log("WebSocket connection closed");
        };
    }

    writeBotMessageDirectly(text) {
        var temp = document.querySelector('.chatbox__messages').firstChild
        for(let i = 0; i < text.length; i++) {
            let index = text.length - i - 1
            setTimeout(function() {
                temp.textContent += text[index]
            }, (text.length - i - 1) * 20);
        }
    }

    showMessage(response) {
        console.log(response)
        const elements = response.message
        for (let index = 0; index < elements.length; index++) {
            if (elements[index] == "please open ws") {
                this.updateChatText("", "bot")
                this.showMessageWebSocketMode()
            }
            else if (elements[index] == "") {
                continue
            }
            else {
                this.updateChatText(elements[index], "bot")
            }
        }
    }

    updatePrice(response) {
        const price = JSON.parse(response.current_price)
        let price_holder = document.querySelector(".cart__footer")

        var html = ""
        html += '<p>هزار تومان</p>\n'
        html += '<p>' + price + '</p>\n'
        html += '<h4 class="cart__footer--header">:قیمت</h4>\n'

        price_holder.innerHTML = html
    }

    updateChatText(message, author) {
        var html = '';
        if (author === "bot")
        {
            html += '<div class="messages__item messages__item--visitor" style="white-space: pre-line">' + message + '</div>'
        }
        else
        {
            html += '<div class="messages__item messages__item--operator">' + message + '</div>'
        }

        const chatmessage = document.querySelector('.chatbox__messages');
        chatmessage.innerHTML = html + chatmessage.innerHTML
    }

    updateCartList(response) {
        const elements = response.content
        const cartlist = document.querySelector(".cart__list")
        var html = ""
        for (let index = 0; index < elements.length; index++) {
            const res = elements[index]
            html += '<div class="cart__item">\n<div class="cart__item__val">' + res[2] + '</div>\n'
            html += '<div class="cart__item__val">' + res[1] + '</div>\n'
            html += '<div class="cart__item__val">' + res[0] + '</div>\n</div>\n'
        }
        cartlist.innerHTML += html
    }

    deleteCart() {
        const cartlist = document.querySelector(".cart__list")
        const cartfooter = document.querySelector(".cart__footer")

        cartlist.innerHTML = ""
        cartfooter.innerHTML = ""
        this.mustToggleCart = false
    }

    deleteFromCart(response) {
        let items = document.querySelectorAll('.cart__item')
        const index = response.deleted

        console.log(index)
        console.log(items)

        if (index >= 0 && index < items.length) {
            items[index].remove();
        }

    }

}


const chatbox = new Chatbox();
chatbox.display();