new Vue({
    el: '#app',
    data: {
        operator: null,
        operatorname: '',
        name: '',
        boards: [],
        remark: '',
        launched: false
    },
    methods: {
        updatebiz: function() {
            let biz = {
                operator: this.operator,
                name: this.name,
                remark: this.remark || null,
                boards: this.boards
            };
            this.$patch(`/rests/bizs/${this.bizid}`, biz).then(res=>{
                this.$toast.show();
            });
        }
    },
    created: function() {
        let bizid = Number(new URL(window.location.href).searchParams.get('bizid'));
        if (!bizid) return;
        this.$get(`/rests/bizs/${bizid}`).then(res => {
            const biz = res.data;
            this.bizid = bizid;
            this.name = biz['name'];
            this.remark = biz['remark'];
            this.boards = biz['boards'];
            this.operator = biz['operator'];
            this.operatorname = biz['operatorname'];
            this.launched = true;
        });
    }
});