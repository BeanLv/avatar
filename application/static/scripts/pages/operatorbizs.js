Vue.use(swipe);
new Vue({
    el: '#app',
    data: {
        operatorid: undefined,
        operatorname: undefined,
        bizs: [],
        launched: false
    },
    methods: {
        editbiz: function (biz) {
            this.editingbiz = biz;
            biz.editing = true;
            biz.newname = '';
            window.$eventbus.$emit('swipeclear');
        },
        canceledit: function (biz) {
            this.editingbiz = null;
            biz.editing = false;
            biz.newname = '';
        },
        updatebiz: function (biz) {
            this.$patch(`/rests/bizs/${biz['id']}`, {name: biz.newname}).then(() => {
                biz.name = biz.newname;
                this.$prompt('成功', '修改成功!');
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
    },
    computed: {
        createbizurl: function () {
            return '/pages/biz'
        },
        disableupdate: function (name) {
            return !name || !/^\S{1,10}$/.test(name);
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
                b.newname = ''
            });
            this.bizs = res.data['bizs'];
            this.editingbiz = null;
            this.launched = true;
        });
    }
});