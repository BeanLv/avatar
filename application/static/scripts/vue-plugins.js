Vue.prototype.$loading = (function () {

    const html = `<div>
                      <div class="weui-mask"></div>
                      <div class="weui-toast">
                          <i class="weui-loading weui-icon_toast"></i>
                          <p class="weui-toast__content"></p>
                      </div>
                  </div>`;

    function _loading() {
        this.$elm = null;
        this.$txt = null;
    }

    _loading.prototype.show = function (text) {
        this.$elm === null && (this.$elm = $(html)) && (this.$txt = this.$elm.find('.weui-toast__content'));
        this.$txt.text(text || '加载中');
        $(document.body).append(this.$elm);
    };

    _loading.prototype.close = function () {
        this.$elm.remove();
    };

    return new _loading();
})();

Vue.prototype.$toast = (function () {

    const html = `<div>
                      <div class="weui-mask_transparent"></div>
                      <div class="weui-toast">
                          <i class="weui-icon-success-no-circle weui-icon_toast"></i>
                          <p class="weui-toast__content"></p>
                      </div>
                  </div>`;

    function _toast() {
        this.$elm = null;
        this.$txt = null;
    }

    _toast.prototype.show = function (text) {
        this.$elm === null && (this.$elm = $(html)) && (this.$txt = this.$elm.find('.weui-toast__content'));
        this.$elm.css({display: 'block', opacity: 1});
        this.$txt.text(text || '成功');
        $(document.body).append(this.$elm);
        window.setTimeout(() => this.$elm.fadeOut(500), 1000);
        window.setTimeout(() => this.$elm.remove(), 1500);
    };

    return new _toast();
})();

Vue.prototype.$prompt = (function () {

    const html = `<div>
                      <div class="weui-mask"></div>
                      <div class="weui-dialog">
                          <div class="weui-dialog__hd">
                              <strong class="weui-dialog__title"></strong>
                          </div>
                          <div class="weui-dialog__bd">
                          </div>
                          <div class="weui-dialog__ft">
                              <a href="javascript:;" class="weui-dialog__btn"></a>
                          </div>
                      </div>
                  </div>`;

    function _prompt() {
        this.$elm = null;
        this.$ttl = null;
        this.$msg = null;
        this.$btn = null;
    }

    _prompt.prototype.show = function (title, msg, iserr, oktxt) {
        this.$elm === null
        && (this.$elm = $(html))
        && (this.$ttl = this.$elm.find('.weui-dialog__title'))
        && (this.$msg = this.$elm.find('.weui-dialog__bd'))
        && (this.$btn = this.$elm.find('.weui-dialog__btn'))
        && (this.$btn.bind('click', () => this.$elm.remove()));
        this.$ttl.text(title);
        this.$msg.text(msg);
        this.$btn.text(oktxt || '确定');
        this.$btn.removeClass('fc-primary').removeClass('fc-warning').addClass(iserr ? 'fc-warning' : 'fc-primary');
        $(document.body).append(this.$elm);
    };

    return new _prompt();
})();

Vue.prototype._$onresponseerr = function (e) {
    if (e.response.status === 401) this.$prompt.show('登录超时', '请刷新页面重新登录', true);
    else if (e.response.status === 403) this.$prompt.show('拒绝访问', '你没有权限这么做', true);
    else this.$prompt.show('错误', '出错啦！请联系管理员', true);
};

Vue.prototype.$get = function (url, options) {
    return new Promise(resolve => {
        this.$loading.show();
        axios.get(url, options).then(res => resolve(res))
            .catch(e => this._$onresponseerr(e))
            .then(() => this.$loading.close());
    });
};

Vue.prototype.$post = function (url, json) {
    return new Promise(resolve => {
        this.$loading.show();
        axios.post(url, json).then(res => resolve(res))
            .catch(e => this._$onresponseerr(e))
            .then(() => this.$loading.close());
    });
};

Vue.prototype.$patch = function (url, json) {
    return new Promise(resolve => {
        this.$loading.show();
        axios.patch(url, json).then(res => resolve(res))
            .catch(e => this._$onresponseerr(e))
            .then(() => this.$loading.close());
    });
};

Vue.prototype.$delete = function (url) {
    return new Promise(resolve => {
        this.$loading.show();
        axios.delete(url).then(res => resolve(res))
            .catch(e => this._$onresponseerr(e))
            .then(() => this.$loading.close());
    });
};

const strtime = {
    filters: {
        strfdate: function (timestampinseconds) {
            const date = new Date(timestampinseconds * 1000);
            const stryear = date.getFullYear().toString();
            const strmonth = (date.getMonth() + 1).toString().padStart(2, '0');
            const strday = date.getDate().toString().padStart(2, '0');
            const strhour = date.getHours().toString().padStart(2, '0');
            const strminutes = date.getMinutes().toString().padStart(2, '0');
            return `${stryear}-${strmonth}-${strday} ${strhour}:${strminutes}`;
        },
        strftime: function (timestampinseconds) {
            const date = new Date(timestampinseconds * 1000);
            const stryear = date.getFullYear().toString();
            const strmonth = (date.getMonth() + 1).toString().padStart(2, '0');
            const strday = date.getDate().toString().padStart(2, '0');
            const hour = date.getHours().toString().padStart(2, '0');
            const minutes = date.getMinutes().toString().padStart(2, '0');
            const seconds = date.getSeconds().toString().padStart(2, '0');
            return `${stryear}/${strmonth}/${strday} ${hour}:${minutes}:${seconds}`;
        }
    }
};

const actionsheet = {
    install: function () {
        Vue.component('actionsheet-item', {
            props: ['name', 'action'],
            data: function () {
                return {
                    actionvalue: null
                }
            },
            methods: {
                choose: function () {
                    this.$parent.chooseaction(this);
                }
            },
            mounted: function () {
                this.actionvalue = this.action.startsWith('number:') ?
                    Number(this.action.replace('number:', '')) :
                    this.action;
            },
            template: `<div class="weui-actionsheet__cell" v-on:click="choose" v-text="name"></div>`
        });

        Vue.component('actionsheet', {
            props: ['name'],
            methods: {
                toggle: function () {
                    this.shown = !this.shown;
                    this.shown ? this.$mask.fadeIn(200) : this.$mask.fadeOut(200);
                    this.$sheet.toggleClass('weui-actionsheet_toggle');
                },
                chooseaction: function (action) {
                    this.$emit('chooseaction', this.name, action)
                }
            },
            mounted: function () {
                this.shown = false;
                this.$mask = $(this.$refs['mask']);
                this.$sheet = $(this.$refs['sheet']);
                this.$refs['root'].parentNode.addEventListener('click', this.toggle);
            },
            beforedestroy: function () {
                this.$refs['root'].parentNode.removeEventListener('click', this.toggle);
            },
            template: `<div ref="root">
                           <div class="weui-mask" style="opacity:0; display:none;" ref="mask"></div>
                           <div class="weui-actionsheet" ref="sheet">
                               <div class="weui-actionsheet__menu">
                                   <slot></slot> 
                               </div>
                               <div class="weui-actionsheet__action fc-warning">
                                   <div class="weui-actionsheet__cell">取消</div>
                               </div>
                           </div>
                       </div>`
        });
    }
};

const confirm = {
    install: function () {
        Vue.component('confirm', {
            props: ['title', 'msg', 'confirmtext', 'canceltext'],
            methods: {
                show: function (title, msg, confirmtxt, canceltxt) {
                    this.$refs['ttl'].innerText = title || this.title || '提示';
                    this.$refs['msg'].innerText = msg || this.msg || '确定这么做么';
                    this.$refs['confirmbtn'].innerText = confirmtxt || this.confirmtext || '确定';
                    this.$refs['cancelbtn'].innerText = canceltxt || this.canceltext || '取消';
                    this.$refs['container'].style.display = 'block';
                    const $this = this;
                    return new Promise(resolve => {
                        $this.resolve = resolve;
                    });
                },
                onconfirm: function () {
                    this.$refs['container'].style.display = 'none';
                    this.resolve && this.resolve();
                    this.resolve = null;
                },
                oncancel: function () {
                    this.$refs['container'].style.display = 'none';
                    this.resolve = null;
                }
            },
            template: `<div ref="container" style="display: none;">
                           <div class="weui-mask"></div>
                           <div class="weui-dialog">
                               <div class="weui-dialog__hd">
                                   <strong class="weui-dialog__title" ref="ttl"></strong>
                               </div>
                               <div class="weui-dialog__bd" ref="msg"></div>
                               <div class="weui-dialog__ft">
                                   <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_default" v-on:click="oncancel" ref="cancelbtn"></a>
                                   <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_primary" v-on:click="onconfirm" ref="confirmbtn"></a>
                               </div>
                           </div>
                       </div>`
        });
    }
};

const order = (function () {

    const ownernames = ['所有', '我自己'];
    const statusnames = ['所有', '待处理', '处理中', '已完成', '已取消', '已关闭'];
    const statuscsses = ['', 'fc-warning_primary', 'fc-info', 'fc-primary', 'fc-warning', 'fc-warning'];
    const operationnames = ['', '创建', '受理', '完成', '取消', '关闭'];
    const operationcsses = ['', 'fc-warning_primary', 'fc-info', 'fc-primary', 'fc-warning', 'fc-warning'];

    return {
        filters: {
            ownername: function (owner) {
                return ownernames[owner];
            },
            statusname: function (status) {
                return statusnames[status];
            },
            statuscss: function (status) {
                return statuscsses[status]
            },
            operationname: function (operation) {
                return operationnames[operation]
            },
            operationcss: function (operation) {
                return operationcsses[operation]
            },
            orderurl: function (orderid) {
                return `/pages/order?orderid=${orderid}`;
            }
        }
    }
})();
