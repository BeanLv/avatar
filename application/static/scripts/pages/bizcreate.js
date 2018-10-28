new Vue({
    el: '#app',
    data: {
        operatorname: '',
        name: '',
        boards: [{
            display: true,
            v1: '',
            v2: '',
            v3: '',
            v4: '',
            v5: '',
            v6: {
                title: '',
                value: ''
            }
        },{
            display: false,
            v1: '',
            v2: '',
            v3: '',
            v4: '',
            v5: '',
            v6: {
                title: '',
                value: ''
            }
        }],
        remark: '',
        launched: false
    },
    methods: {
        createbiz: function() {
            let biz = {
                operator: this.operatorid,
                name: this.name,
                remark: this.remark || null,
                boards: this.boards
            };
            this.$post(`/rests/bizs`, biz).then(res=>{
                window.location.href = `/public/pages/bizs/${res.data}`;
            });
        },
        reset: function() {
            this.name = '';
            this.remark = '';
            this.boards = [{
                display: true,
                v1: '',
                v2: '',
                v3: '',
                v4: '',
                v5: '',
                v6: { title: '', value: '' }
            },{
                display: false,
                v1: '',
                v2: '',
                v3: '',
                v4: '',
                v5: '',
                v6: { title: '', value: '' }
            }];
        }
    },
    created: function() {
        let operatorid = Number(new URL(window.location.href).searchParams.get('operatorid'));
        if (!operatorid) return;
        this.$get(`/rests/operators/${operatorid}`).then(res => {
            const operator = res.data;
            this.operatorid = operator['id'];
            this.operatorname = operator['name'];
            this.launched = true;
        });
    }
});