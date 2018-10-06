Vue.use(confirm);
Vue.component('weui-cell-swipe', {
    props: ['id', 'name', 'foot', 'href', 'index'],
    data: function () {
        return {
            newname: '',
            state: 'normal',
            editing: false
        }
    },
    methods: {
        ontouchstart: function ($e) {
            if (this.iter || $e.touches.length > 1) return;
            if (this.state === 'normal') {
                this.state = 'swiping';
                this.btn1x = Math.ceil(this.btn1x);
                this.btn2x = -60 + 2 * (this.btn1x + 60);
                this.btn1.style.right = this.btn1x + 'px';
                this.btn2.style.right = this.btn2x + 'px';
                this.x = $e.targetTouches[0].screenX;
                this.$root.swipestart(this);
            } else {
                this.swipin();
            }
        },
        ontouchmove: function ($e) {
            if (this.state !== 'swiping') return;
            if ($e.targetTouches[0].screenX < this.x) {
                this.btn1x = Math.min(60, this.btn1x + 2);
                this.btn2x = Math.min(0, this.btn2x + 1);
            } else {
                this.btn1x = Math.max(-60, this.btn1x - 2);
                this.btn2x = Math.max(-60, this.btn2x - 1);
            }
            this.btn1.style.right = this.btn1x + 'px';
            this.btn2.style.right = this.btn2x + 'px';
            this.x = $e.targetTouches[0].screenX;
            $e.preventDefault();
            return false;
        },
        ontouchend: function () {
            if (this.state !== 'swiping') return;
            this.btn2x >= -55 ? this.swipout() : this.swipin();
        },
        beforejump: function ($e) {
            const notjump = this.btn2x >= -55;
            notjump && $e.preventDefault();
            return !notjump;
        },
        blur: function () {
            this.editing = false;
            this.state !== 'normal' && this.swipin();
        },
        swipout: function () {
            this.state = 'swipeout';
            this.iter = window.setInterval(() => {
                this.btn1x = Math.min(60, this.btn1x + 2);
                this.btn2x = Math.min(0, this.btn2x + 1);
                this.btn1.style.right = this.btn1x + 'px';
                this.btn2.style.right = this.btn2x + 'px';
                this.btn2x === 0 && (window.clearInterval(this.iter) || (this.iter = null));
            }, 5);
        },
        swipin: function () {
            this.state = 'normal';
            this.iter = window.setInterval(() => {
                this.btn1x = Math.max(-60, this.btn1x - 2);
                this.btn2x = Math.max(-60, this.btn2x - 1);
                this.btn1.style.right = this.btn1x + 'px';
                this.btn2.style.right = this.btn2x + 'px';
                this.btn2x === -60 && (window.clearInterval(this.iter) || (this.iter = null));
            }, 5);
        },
        edit: function () {
            this.newname = '';
            this.editing = true;
            this.$refs.input.focus();
        },
        cancel: function () {
            this.newname = '';
            this.editing = false;
        },
        update: function () {
            this.$emit('swipeupdate', {
                id: this.id,
                name: this.newname,
                index: this.index
            });
        },
        confirmdelete: function () {
            this.$refs['confirm'].show('提示', '确定删除么？').then(() => this.$emit('swipedelete', {
                id: this.id,
                index: this.index
            }));
        }
    },
    computed: {
        disableupdate: function () {
            return !this.newname || this.newname === this.name || !/^\S{1,10}$/.test(this.newname);
        },
        jumpto: function () {
            return this.href || 'javascript:;';
        },
    },
    mounted: function () {
        this.btn1 = this.$refs.btn1;
        this.btn2 = this.$refs.btn2;
        this.btn1x = -60;
        this.btn2x = -60;
    },
    template: `
<div class="weui-cell weui-cell_swiped" v-bind:class="state">
    <div class="weui-cell__bd">
             <div class="weui-cell weui-cell_form" v-show="editing">
                <div class="weui-cell__bd">
                    <input type="text" maxlength="10" class="weui-input" v-model="newname"
                           placeholder="输入新名称" ref="input">
                </div>
                <div class="weui-cell__ft">
                    <button type="button" class="weui-cell-btn bg-primary" v-on:click="update"
                            v-bind:disabled="disableupdate">确定</button><!--
                --><button type="button" class="weui-cell-btn bg-warn" v-on:click="cancel">取消</button>
                </div>
            </div>
            <a v-show="!editing" class="weui-cell weui-cell_access" v-bind:href.once="jumpto"
               v-on:click="beforejump($event)" v-on:touchstart="ontouchstart($event)"
               v-on:touchmove="ontouchmove($event)" v-on:touchend="ontouchend()">
                <div class="weui-cell__bd">
                    <p>{{ name }}</p>
                </div>
                <div class="weui-cell__ft">{{ foot }}</div>
            </a>
        </div>
    <div class="weui-cell__ft" v-show="!editing">
        <button class="weui-cell_swipe-btn bg-info_primary" style="right:-60px;" ref="btn1"
                v-on:click="edit">编辑</button>
        <button class="weui-cell_swipe-btn bg-warn" style="right:-60px;" ref="btn2"
                v-on:click="confirmdelete">删除</button>
    </div>
    <confirm ref="confirm"></confirm>
</div>`
});