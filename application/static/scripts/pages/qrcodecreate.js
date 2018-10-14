Vue.use(addressbook);
new Vue({
    el: '#app',
    mixins: [mixins.qrcode],
    data: {
        name: '',
        owner: null,
        remark: '',
        launched: false
    },
    methods: {
        chooseowner: function () {
            this.$refs['addressbook'].show().then(owner => {
                this.owner = owner;
            });
        },
        createqrcode: function () {
            this.$post('/rests/qrcodes', {
                name: this.name,
                owner: this.owner.id,
                remark: this.remark
            }).then(res => {
                if (res.status === 204) {
                    this.$prompt('错误', res.data, true);
                } else {
                    window.location.href = `/public/pages/qrcodes/${res.data}`;
                }
            });
        }
    },
    computed: {
        disablecreate: function () {
            return this.isinvalidname(this.name) ||
                this.owner === null;
        }
    },
    created: function () {
        this.launched = true;
    }
});