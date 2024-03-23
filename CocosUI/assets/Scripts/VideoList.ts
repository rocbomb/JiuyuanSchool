import { _decorator, Component, Node ,Prefab, instantiate, ScrollView} from 'cc';
const { ccclass, property } = _decorator;
import { log } from 'cc';



@ccclass('VideoItem')
export class VideoItem {
    @property
    id = 0;

    @property
    itemName = '';

    @property
    itemTime = 0;

    @property
    isOk = false;
}


@ccclass('VideoList')
export class VideoList extends Component {
    @property([VideoItem])
    items: VideoItem[] = [];
    @property(Prefab)
    itemPrefab: Prefab | null = null;

    @property(ScrollView)
    scrollView: ScrollView

    onLoad() {
        for (let i = 0; i < this.items.length; ++i) {
            const item = instantiate(this.itemPrefab);
            const data = this.items[i];
            log("VideoList Load" + data.itemName)
            this.scrollView.content.addChild(item);
            item.getComponent('ItemTemplate').init(data);
        }
    }
}


