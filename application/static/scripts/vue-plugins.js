window.$eventbus = new Vue();

Vue.prototype.$loading = (function () {

    const html = `<div>
                      <div class="weui-mask" style="z-index: 5000"></div>
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
        this.$btn.removeClass('fc-primary').removeClass('fc-warn').addClass(iserr ? 'fc-warn' : 'fc-primary');
        $(document.body).append(this.$elm);
    };

    return new _prompt();
})();

Vue.prototype.$confirm = (function () {

    const html = `<div>
                       <div class="weui-mask"></div>
                       <div class="weui-dialog">
                           <div class="weui-dialog__hd">
                               <strong class="weui-dialog__title"></strong>
                           </div>
                           <div class="weui-dialog__bd"></div>
                           <div class="weui-dialog__ft">
                               <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_default"></a>
                               <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_primary"></a>
                           </div>
                       </div>
                   </div>`;

    function _confirm() {
        this.$elm = null;
        this.$ttl = null;
        this.$msg = null;
        this.$no = null;
        this.$yes = null;
        this.resolve = null;
    }

    _confirm.prototype.show = function (ttl, msg, no, yes) {
        if (this.$elm === null) {
            this.$elm = $(html);
            this.$ttl = this.$elm.find('.weui-dialog__title');
            this.$msg = this.$elm.find('.weui-dialog__bd');
            this.$no = this.$elm.find('.weui-dialog__btn_default');
            this.$yes = this.$elm.find('.weui-dialog__btn_primary');
            this.$no.bind('click', () => {
                this.resolve = null;
                this.$elm.remove();
            });
            this.$yes.bind('click', () => {
                const resolve = this.resolve;
                this.resolve = null;
                this.$elm.remove();
                resolve();
            });
        }
        this.$ttl.text(ttl || '提示');
        this.$msg.text(msg || '确定这么做么');
        this.$no.text(no || '取消');
        this.$yes.text(yes || '确定');
        return new Promise(resolve => {
            this.resolve = resolve;
            $(document.body).append(this.$elm);
        });
    };

    return new _confirm();
})();

Vue.prototype.$choice = (function () {

    const html = `<div>
                       <div class="weui-mask"></div>
                       <div class="weui-dialog">
                           <div class="weui-dialog__hd">
                               <strong class="weui-dialog__title"></strong>
                           </div>
                           <div class="weui-dialog__bd"></div>
                           <div class="weui-dialog__ft">
                               <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_default"></a>
                               <a href="javascript:;" class="weui-dialog__btn weui-dialog__btn_primary"></a>
                           </div>
                       </div>
                   </div>`;

    function _choice() {
        this.$elm = null;
        this.$ttl = null;
        this.$msg = null;
        this.$no = null;
        this.$yes = null;
        this.resolve = null;
        this.reject = null;
    }

    _choice.prototype.show = function (ttl, msg, no, yes) {
        if (this.$elm === null) {
            this.$elm = $(html);
            this.$ttl = this.$elm.find('.weui-dialog__title');
            this.$msg = this.$elm.find('.weui-dialog__bd');
            this.$no = this.$elm.find('.weui-dialog__btn_default');
            this.$yes = this.$elm.find('.weui-dialog__btn_primary');
            this.$no.bind('click', () => {
                const reject = this.reject;
                this.resolve = this.reject = null;
                this.$elm.remove();
                reject();
            });
            this.$yes.bind('click', () => {
                const resolve = this.resolve;
                this.resolve = this.reject = null;
                this.$elm.remove();
                resolve();
            });
        }
        this.$ttl.text(ttl || '提示');
        this.$msg.text(msg || '确定这么做么');
        this.$no.text(no || '取消');
        this.$yes.text(yes || '确定');
        return new Promise((resolve, reject) => {
            this.resolve = resolve;
            this.reject = reject;
            $(document.body).append(this.$elm);
        });
    };

    return new _choice();
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

const hiddenpage = (function () {
    return {
        install: function (Vue) {
            Vue.component('hidden-page', {
                methods: {
                    show: function () {
                        $(this.$refs['mask']).css('display', 'block');
                        let $page = $(this.$refs['page']);
                        $page.addClass('hidden-page__on');
                        $('#app').css({
                            'overflow': 'hidden',
                            'height': `${$page.height()}px`
                        });
                    },
                    close: function () {
                        $(this.$refs['mask']).css('display', 'none');
                        let $page = $(this.$refs['page']);
                        $page.removeClass('hidden-page__on');
                        let $app = $('#app');
                        $app.prop('style').removeProperty('overflow');
                        $app.prop('style').removeProperty('height');
                    }
                },
                template: `<div>
                               <div class="weui-mask" style="display: none" ref="mask"></div>
                               <div class="hidden-page" ref="page">
                                   <slot></slot>
                                </div>
                            </div>`
            });
        }
    }
})();

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
            beforeDestroy: function () {
                this.$refs['root'].parentNode.removeEventListener('click', this.toggle);
            },
            template: `<div ref="root">
                           <div class="weui-mask" style="opacity:0; display:none;" ref="mask"></div>
                           <div class="weui-actionsheet" ref="sheet">
                               <div class="weui-actionsheet__menu">
                                   <slot></slot> 
                               </div>
                               <div class="weui-actionsheet__action fc-warn">
                                   <div class="weui-actionsheet__cell">取消</div>
                               </div>
                           </div>
                       </div>`
        });
    }
};

const swipe = (function () {
    const SWIPEOUT = 0;
    const SWIPEIN = 1;
    const SWIPING = 2;
    const AUTOSWIPEOUT = 3;
    const AUTOSWIPEIN = 4;
    return {
        install: function (Vue) {
            Vue.component('swipe', {
                props: ['href'],
                methods: {
                    ontouchstart: function ($event) {
                        if (this.s === SWIPEIN) {
                            this.autoswipeout();
                        } else if (this.s === SWIPEOUT) {
                            this.s = SWIPING;
                            this.setswipeoutcss();
                            this.x = $event.targetTouches[0].screenX;
                            this.o = $event.targetTouches[0].screenX;
                            this.t = this.$width;
                            window.$eventbus.$emit('swipestart', this);
                        }
                    },
                    ontouchmove: function ($event) {
                        if (this.s === SWIPING) {
                            const x = $event.targetTouches[0].screenX;
                            (x < this.x) ? this.t -= 1 : this.t += 1;
                            this.t = Math.max(0, Math.min(this.$width, this.t));
                            this.$swiper.css('transform', `translateX(${this.t}px)`);
                            this.x = x;
                        }
                    },
                    ontouchend: function () {
                        if (this.s === SWIPING) {
                            const swipeleftdistance = this.o - this.x;
                            if (swipeleftdistance <= 10) {
                                this.s = SWIPEOUT;
                                this.setswipeoutcss();
                            } else if (swipeleftdistance < 30) {
                                this.autoswipeout();
                            } else {
                                this.autoswipein();
                            }
                        }
                    },
                    autoswipein: function () {
                        this.s = AUTOSWIPEIN;
                        this.setswipeincss(true);
                        this.i = window.setTimeout(() => this.s = SWIPEIN, 300);
                    },
                    autoswipeout: function () {
                        this.s = AUTOSWIPEOUT;
                        this.setswipeoutcss(true);
                        this.i = window.setTimeout(() => this.s = SWIPEOUT, 300);
                    },
                    onswipestart: function (swipecell) {
                        if (this !== swipecell) {
                            if (this.s === AUTOSWIPEIN) {
                                this.i && window.clearTimeout(this.i);
                                this.autoswipeout();
                            } else if (this.s === SWIPEIN) {
                                this.autoswipeout();
                            }
                        }
                    },
                    onswipeclear: function (transition) {
                        if (this.s === SWIPEIN) {
                            if (transition) {
                                this.autoswipeout();
                            } else {
                                this.s = SWIPEOUT;
                                this.setswipeoutcss();
                            }
                        } else if (this.s === AUTOSWIPEIN) {
                            this.i && window.clearTimeout(this.i);
                            if (transition) {
                                this.autoswipeout();
                            } else {
                                this.s = SWIPEOUT;
                                this.setswipeoutcss();
                            }
                        }
                    },
                    setswipeincss: function (transition) {
                        if (transition) {
                            this.$swiper.css({transform: 'translateX(0)', transition: 'transform, .3s'});
                        } else {
                            this.$swiper.css({transform: 'translateX(0)', transition: 'none'});
                        }
                    },
                    setswipeoutcss: function (transition) {
                        if (transition) {
                            this.$swiper.css({transform: `translateX(${this.$width}px)`, transition: 'transform, .3s'});
                        } else {
                            this.$swiper.css({transform: `translateX(${this.$width}px)`, transition: 'none'});
                        }
                    },
                    beforejump: function ($event) {
                        if (this.s !== SWIPEOUT) {
                            $event.preventDefault();
                            return false;
                        }
                    },
                },
                mounted: function () {
                    this.i = null;
                    this.s = SWIPEOUT;
                    const root = this.$refs['root'];
                    this.trigger = root.querySelector('.weui-cell__swipetrigger');
                    this.trigger.addEventListener('touchstart', this.ontouchstart);
                    this.trigger.addEventListener('touchmove', this.ontouchmove);
                    this.trigger.addEventListener('touchend', this.ontouchend);
                    this.$swiper = $(root.querySelector('.weui-cell__swiper'));
                    this.$swiper.css('transform', `translateX(${this.$swiper.width()}px)`);
                    this.$width = this.$swiper.width();
                    window.$eventbus.$on('swipestart', this.onswipestart);
                    window.$eventbus.$on('swipeclear', this.onswipeclear);
                },
                beforeDestroy() {
                    this.trigger.removeEventListener('touchstart', this.ontouchstart);
                    this.trigger.removeEventListener('touchmove', this.ontouchmove);
                    this.trigger.removeEventListener('touchend', this.ontouchend);
                    window.$eventbus.$off('swipestart', this.onswipestart);
                    window.$eventbus.$off('swipeclear', this.onswipeclear);
                },
                computed: {
                    jumpurl: function () {
                        return this.href || 'javascript:;';
                    }
                },
                template: '<a ref="root" v-bind:href.once="jumpurl" v-on:click="beforejump"><slot></slot></a>'
            });
        }
    }
})();

const addressbook = (function () {
    return {
        install: function (Vue) {
            Vue.component('address-book', {
                props: ['allowall', 'title'],
                data: function () {
                    return {
                        groups: [],
                        opened: false,
                        inited: false
                    }
                },
                methods: {
                    initgroups: function () {
                        return new Promise(resolve => {
                            if (this.inited) {
                                resolve();
                            } else {
                                this.$get('/rests/users').then(res => {
                                    let groupdict = {}, grouplist = [];
                                    res.data.forEach(u => {
                                        let firstletter = u['pinying'][0].toUpperCase();
                                        let users = groupdict[firstletter];
                                        if (!users) {
                                            users = [];
                                            groupdict[firstletter] = users;
                                        }
                                        users.push(u)
                                    });
                                    Object.keys(groupdict).forEach(g => {
                                        groupdict[g].sort((a, b) => a['pinying'] < b['pinying'] ? -1 : 1);
                                        grouplist.push({name: g, users: groupdict[g]});
                                    });
                                    grouplist.sort((a, b) => a['name'] < b['name'] ? -1 : 1);
                                    this.groups = grouplist;
                                    this.inited = true;
                                    resolve();
                                });
                            }
                        })
                    },
                    show: function () {
                        return new Promise(resolve => {
                            this.resolve = resolve;
                            this.initgroups().then(() => this.opened = true);
                        });
                    },
                    chooseuser: function (u) {
                        this.opened = false;
                        const r = this.resolve;
                        this.resolve = null;
                        r(u);
                    },
                    chooseall: function () {
                        this.opened = false;
                        const r = this.resolve;
                        this.resolve = null;
                        r(null);
                    },
                    cancel: function () {
                        this.resolve = null;
                        this.opened = false;
                    }
                },
                template: `<div class="select-page address-book" v-bind:class="{'select-page__on':opened}">
                               <div class="select-page__title bg-info">
                                   <a class="select-page__title__btn" v-on:click="cancel">取消</a>
                                   <div class="select-page__title__bd">{{ title }}</div>
                               </div>
                               <div class="weui-cells__title" v-if="allowall">全体</div>
                               <div class="weui-cells" v-if="allowall">
                                  <a href="javascript:;" class="weui-cell weui-cell_access" v-on:click="chooseall">
                                      <div class="weui-cell__bd">所有人</div>
                                  </a>
                               </div>
                               <div v-for="g in groups">
                                   <div class="weui-cells__title">{{ g.name }}</div>
                                   <div class="weui-cells">
                                       <a href="javascript:;" class="weui-cell weui-cell_access" 
                                          v-for="u in g.users" v-on:click="chooseuser(u)">
                                           <div class="weui-cell__hd">
                                               <img v-bind:src.once="u.headimgurl" alt="">
                                           </div>
                                           <div class="weui-cell__bd">{{ u.name }}</div>
                                       </a>                                        
                                   </div>
                               </div>
                           </div>`,
            });
        }
    }
})();

const qrcodeselect = (function () {
    return {
        install: function (Vue) {
            Vue.component('qrcode-select', {
                props: ['allowall', 'title'],
                data: function () {
                    return {
                        qrcodes: undefined,
                        opened: false,
                    };
                },
                methods: {
                    initqrcodes: function () {
                        return new Promise(resolve => {
                            if (this.qrcodes !== undefined) {
                                resolve();
                            } else {
                                this.$get('/rests/qrcodes').then(res => {
                                    this.qrcodes = res.data;
                                    resolve();
                                });
                            }
                        });
                    },
                    show: function () {
                        return new Promise(resolve => {
                            this.resolve = resolve;
                            this.initqrcodes().then(() => this.opened = true);
                        });
                    },
                    close: function () {
                        this.resolve = null;
                        this.opened = false;
                    },
                    chooseqrcode: function (qrcode) {
                        this.opened = false;
                        const resolve = this.resolve;
                        this.resolve = null;
                        resolve(qrcode);
                    },
                    chooseall: function () {
                        this.opened = false;
                        const resolve = this.resolve;
                        this.resolve = null;
                        resolve(null);
                    }
                },
                template: `<div class="select-page" v-bind:class="{'select-page__on':opened}">
                               <div class="select-page__title bg-info">
                                   <a class="select-page__title__btn" v-on:click="close">取消</a>
                                   <div class="select-page__title__bd">{{ title }}</div>
                               </div>
                               <div class="weui-cells__title" v-if="allowall">全部</div>
                               <div class="weui-cells" v-if="allowall">
                                   <a class="weui-cell weui-cell_access" v-on:click="chooseall">
                                       <div class="weui-cell__bd">所有</div>
                                   </a>
                               </div>
                               <div class="weui-cells__title">二维码</div>
                               <div class="weui-cells">
                                   <a class="weui-cell weui-cell_access" v-for="qrcode in qrcodes" v-on:click="chooseqrcode(qrcode)">
                                       <div class="weui-cell__bd">{{ qrcode.name }}</div>
                                   </a>
                               </div>
                           </div>`
            });
        }
    }
})();

const mixins = {
    strtime: {
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
    },
    order: (function () {
        const statusnames = ['所有', '待处理', '处理中', '已完成', '已取消', '已关闭'];
        const statuscsses = ['', 'fc-warn_primary', 'fc-info', 'fc-primary', 'fc-warn', 'fc-warn'];
        const operationnames = ['', '创建', '受理', '完成', '取消', '关闭'];
        const operationcsses = ['', 'fc-warn_primary', 'fc-info', 'fc-primary', 'fc-warn', 'fc-warn'];

        return {
            filters: {
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
    })(),
    biz: (function () {
        const namereg = /^\S{1,10}$/;
        return {
            filters: {
                namecss: function (name) {
                    return (name && namereg.test(name) ) ? '' : 'weui-icon-warn';
                },
                propcss: function (prop) {
                    return (prop && propreg.test(prop) ) ? '' : 'weui-icon-warn';
                }
            },
            methods: {
                getdefaultproperties: function () {
                    return [
                        {name: 'cost', value: ''},
                        {name: 'i1', value: ''},
                        {name: 'i2', value: ''},
                        {name: 'i3', value: ''},
                        {name: 'i4', value: ''},
                        {name: 'i5', value: ''}
                    ];
                },
                isinvalidname: function (name) {
                    return !name || !namereg.test(name);
                },
                isinvalidprop: function (prop) {
                    return !prop || prop.length > 20;
                }
            }
        };
    })(),
    qrcode: (function () {
        const namereg = /^\S{1,10}$/;
        return {
            filters: {
                ownername: function (owner) {
                    return owner ? owner.name : '选择负责人';
                },
                ownernamecss: function (owner) {
                    return owner ? 'fc-default' : 'fc-secondary';
                },
                ownercss: function (owner) {
                    return owner ? '' : 'weui-icon-warn';
                },
                namecss: function (name) {
                    return (name && namereg.test(name)) ? '' : 'weui-icon-warn';
                }
            },
            methods: {
                isinvalidname: function (name) {
                    return !name || !namereg.test(name);
                }
            }
        }
    })(),
};

