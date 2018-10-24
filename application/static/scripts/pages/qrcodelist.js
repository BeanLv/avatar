Vue.use(swipe);
Vue.use(addressbook);
Vue.use(hiddenpage);
new Vue({
    el: '#app',
    data: {
        qrcodes: [],
        editpage: {
            qrcode: {id: '', name: '', owner: '', ownername: '', remark: ''},
            name: '',
            owner: '',
            ownername: '',
            remark: ''
        },
        createpage: {
            name: '',
            owner: '',
            ownername: '',
            remark: ''
        },
        launched: false
    },
    methods: {
        entereditmode: function (qrcode) {
            this.editpage.qrcode = qrcode;
            this.editpage.name = qrcode.name;
            this.editpage.owner = qrcode.owner;
            this.editpage.ownername = qrcode.ownername;
            this.editpage.remark = qrcode.remark;
            this.$refs['editpage'].show();
            window.$eventbus.$emit('swipeclear', true);
        },
        exiteditmode: function () {
            this.$refs['editpage'].close();
        },
        changeowner: function () {
            this.$refs['changeowner'].show().then(owner => {
                this.editpage.owner = owner.id;
                this.editpage.ownername = owner.name;
            });
        },
        updateqrcode: function () {
            this.$refs['editpage'].close();
            const qrcode = {
                name: this.editpage.name,
                owner: this.editpage.owner,
                remark: this.editpage.remark || null
            };
            this.$patch(`/rests/qrcodes/${this.editpage.qrcode.id}`, qrcode).then(() => {
                this.editpage.qrcode.name = this.editpage.name;
                this.editpage.qrcode.owner = this.editpage.owner;
                this.editpage.qrcode.ownername = this.editpage.ownername;
                this.editpage.qrcode.remark = this.editpage.remark;
                this.$toast.show();
            });
        },
        entercreatemode: function () {
            this.createpage.name = '';
            this.createpage.owner = '';
            this.createpage.ownername = '';
            this.createpage.remark = '';
            this.$refs['createpage'].show();
            window.$eventbus.$emit('swipeclear', true);
        },
        exitcreatemode: function () {
            this.$refs['createpage'].close();
        },
        chooseowner: function () {
            this.$refs['chooseowner'].show().then(owner => {
                this.createpage.owner = owner.id;
                this.createpage.ownername = owner.name;
            });
        },
        createqrcode: function () {
            this.$refs['createpage'].close();
            const qrcode = {
                name: this.createpage.name,
                owner: this.createpage.owner,
                remark: this.createpage.remark || null
            };
            this.$post('/rests/qrcodes', qrcode).then(res => {
                qrcode.id = res.data;
                qrcode.ownername = this.createpage.ownername;
                this.qrcodes.push(qrcode);
                this.$toast.show();
            });
        }
    },
    filters: {
        qrcodepreviewurl: function (qrcode) {
            return `/public/pages/qrcodes/${qrcode.id}`
        },
        ownername: function (name) {
            return name ? name : '选择负责人';
        },
        namecss: function (name) {
            return (name && /^\S{1,10}$/.test(name)) ? '' : 'weui-icon-warn';
        },
        ownercss: function (owner) {
            return owner ? '' : 'weui-icon-warn';
        }
    },
    computed: {
        disableupdateqrcode: function () {
            const p = this.editpage;
            return !p.name || !/^\S{1,10}$/.test(p.name) || !p.owner ||
                (
                    p.qrcode.name === p.name &&
                    p.qrcode.owner === p.owner &&
                    p.qrcode.remark === p.remark
                );
        },
        disablecreateqrcode: function () {
            const p = this.createpage;
            return !p.name || !p.owner;
        }
    },
    created: function () {
        this.$get('/rests/qrcodes').then(res => {
            res.data.forEach(q => q.remark = q.remark || '');
            this.qrcodes = res.data;
            this.launched = true;
        });
    }
});
