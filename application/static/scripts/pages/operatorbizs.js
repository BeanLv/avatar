Vue.use(swipe);
new Vue({
    el: '#app',
    data: {
        operatorid: undefined,
        operatorname: undefined,
        bizs: [],
        editingbiz: null,
        launched: false
    },
    methods: {
        editbiz: function (biz) {
            biz.editing = true;
            biz.newname = '';
            this.editingbiz = biz;
        },
        canceleditbiz: function (biz) {
            biz.editing = false;
            biz.newname = '';
            this.editingbiz = null;
            window.$eventbus.$emit('swipeclear', true);
        },
        updatebiz: function (biz) {
            this.$patch(`/rests/bizs/${biz['id']}`, {name: biz.newname}).then(() => {
                biz.name = biz.newname;
                this.$prompt.show('成功', '编辑成功');
            });
        },
        deletebiz: function (biz, index) {
            this.$confirm.show('提示', '确定要删除么?')
                .then(() => this.$delete(`/rests/bizs/${biz['id']}`))
                .then(() => {
                    this.bizs.splice(index, 1);
                    this.$prompt.show('成功', '删除成功');
                });
        }
    },
    filters: {
        bizdetailurl: function (biz) {
            return `/pages/biz?bizid=${biz['id']}`;
        },
        disableupdatebiz: function (biz) {
            return !biz.newname || (biz.name === biz.newname) || !/^\S{1,10}$/.test(biz.newname);
        }
    },
    computed: {
        createbizurl: function () {
            return '/pages/biz'
        }
    },
    created: function () {
        let operatorid = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!operatorid) return;
        this.$get(`/rests/operators/${operatorid}/bizs`).then(res => {
            this.operatorid = operatorid;
            this.operatorname = res.data['operatorname'];
            res.data['bizs'].forEach(b => {
                b.editing = false;
                b.newname = '';
            });
            this.bizs = res.data['bizs'];
            this.launched = true;
        });
    }
});