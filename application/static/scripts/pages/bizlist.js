Vue.use(swipe);
Vue.use(hiddenpage);
new Vue({
    el: '#app',
    data: {
        operatorid: undefined,
        operatorname: undefined,
        bizs: [],
        editpage: {
            biz: {name: '', operator: null, cost: 0, i1: '', i2: '', i3: '', i4: '', i5: '', remark: ''},
            name: '',
            operator: null,
            cost: 0,
            i1: '',
            i2: '',
            i3: '',
            i4: '',
            i5: '',
            remark: ''
        },
        createpage: {name: '', operator: null, cost: 0, i1: '', i2: '', i3: '', i4: '', i5: '', remark: ''},
        bizproperties: ['name', 'operator', 'cost', 'remark', 'i1', 'i2', 'i3', 'i4', 'i5'],
        launched: false
    },
    methods: {
        entereditmode: function (b) {
            this.editpage.biz = b;
            this.bizproperties.forEach(p => this.editpage[p] = b[p]);
            this.$refs['editpage'].show();
            window.$eventbus.$emit('swipeclear', true);
        },
        exiteditmode: function () {
            this.$refs['editpage'].close();
        },
        updatebiz: function () {
            this.$refs['editpage'].close();
            let newbiz = {};
            this.bizproperties.forEach(p => newbiz[p] = this.editpage[p] || null);
            this.$patch(`/rests/bizs/${this.editpage.biz.id}`, newbiz).then(() => {
                this.bizproperties.forEach(p => this.editpage.biz[p] = this.editpage[p]);
                this.$toast.show();
            });
        },
        entercreatemode: function () {
            this.bizproperties.forEach(p => this.createpage[p] = null);
            this.createpage.operator = this.operatorid;
            this.createpage.remark = '';
            this.$refs['createpage'].show();
            window.$eventbus.$emit('swipeclear', true);
        },
        exitcreatemode: function () {
            this.$refs['createpage'].close();
        },
        createbiz: function () {
            this.$refs['createpage'].close();
            let biz = {};
            this.bizproperties.forEach(p => biz[p] = this.createpage[p]);
            this.$post('/rests/bizs', biz).then(res => {
                biz.id = res.data;
                this.bizs.push(biz);
                this.$toast.show();
            });
        },
        deletebiz: function (biz, index) {
            this.$confirm.show('提示', '确定要删除么?')
                .then(() => this.$delete(`/rests/bizs/${biz['id']}`))
                .then(() => {
                    this.bizs.splice(index, 1);
                    this.$toast.show();
                });
        }
    },
    filters: {
        bizdetailurl: function (biz) {
            return `/public/pages/bizs/${biz['id']}`;
        },
        costcss: function (cost) {
            return (cost && cost > 0) ? '' : 'weui-icon-warn';
        },
        propcss: function (prop) {
            return (prop && prop.trim()) ? '' : 'weui-icon-warn';
        }
    },
    computed: {
        createbizurl: function () {
            return `/pages/bizcreate?operatorid=${this.operatorid}`;
        },
        disableupdatebiz: function () {
            const p = this.editpage;
            return !p.name || !p.cost || !p.i1 || !p.i2 || !p.i3 || !p.i4 || !p.i5 ||
                (
                    p.name === p.biz.name &&
                    p.cost === p.biz.cost &&
                    p.i1 === p.biz.i1 &&
                    p.i2 === p.biz.i2 &&
                    p.i3 === p.biz.i3 &&
                    p.i4 === p.biz.i4 &&
                    p.i5 === p.biz.i5 &&
                    p.remark === p.biz.remark
                )
        },
        disablecreatebiz: function () {
            const p = this.createpage;
            return !p.name || !p.cost || !p.i1 || !p.i2 || !p.i3 || !p.i4 || !p.i5;
        }
    },
    created: function () {
        let operatorid = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!operatorid) return;
        this.$get(`/rests/operators/${operatorid}/bizs`).then(res => {
            res.data['bizs'].forEach(b => b.remark = b.remark || '');
            this.operatorid = operatorid;
            this.operatorname = res.data['operatorname'];
            this.bizs = res.data['bizs'];
            this.launched = true;
        });
    }
});