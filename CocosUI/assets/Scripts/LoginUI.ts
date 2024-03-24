import { _decorator, Component, Node } from 'cc';
import { Button, EditBox, EventHandler, log } from 'cc';
const { ccclass, property } = _decorator;

@ccclass('LoginUI')
export class LoginUI extends Component {

    @property(Node)
    public loginUI:EditBox

    @property(Node)
    public mainUI:EditBox

    @property(EditBox)
    public userId:EditBox

    @property(EditBox)
    public userKey:EditBox

    @property(Button)
    public loginBtn:Button

    start() {
        const clickEventHandler = new EventHandler();
        clickEventHandler.target = this.node; // 这个 node 节点是你的事件处理代码组件所属的节点
        clickEventHandler.component = 'LoginUI';// 这个是脚本类名
        clickEventHandler.handler = 'callback';
        this.loginBtn.clickEvents.push(clickEventHandler);
    }


    callback (event: Event, customEventData: string) {
        log("login " + this.userId.string)
        const userId = this.userId.string
        if(userId === null || userId.trim() === '')
        {
            log("登录失败")
            return
        }
        const userKey = this.userKey.string

        fetch("http://127.0.0.1:8080").then((response: Response) => {
            return response.text()
        }).then((value) => {
            console.log(value);
        })

    }
}
