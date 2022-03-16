<template lang="pug">

.footer
    .container
        .left
            .link О нас
            .link Контакты
            .address {{ contacts.address }}
        .right
            a.phone(:href="`tel:${contacts.phone}`") {{ contacts.phone }}
            .social
                a.social-link(:href="contacts.instagram" tagret="_blank")
                    g-icon(name="ui/instagram")
                a.social-link(:href="contacts.telegram" tagret="_blank")
                    g-icon(name="ui/telegram")
    

</template>
<script>
export default {
    computed: {
        contacts() {
            return this.$store.state.content.contacts
        }
    }
}
</script>
<style lang="stylus" scoped>

.footer
    padding 50px 0 30px
    background-color #2D2F34
    color #fff
    margin-top auto
    +$tablet()
        padding 15px 0
    +$phone()
        padding 15px 16px

.container
    width $desktop-width
    margin auto
    display flex
    justify-content space-between
    align-items stretch
    +$tablet()
        width $tablet-width
    +$phone()
        width 100%

.link
    margin-top 10px
    font-size 16px
    line-height 20px
    color #F4F4F4
    &:first-child
        margin-top 0
    +$phone()
        font-size 14px
        line-height 18px
        margin-top 8px
.address
    margin-top 35px
    font-size 13px
    line-height 17px
    color #A9ACAD
    +$phone()
        font-size 14px
        line-height 18px

.right
    display flex
    flex-direction column
    align-items flex-end
.phone
    font-size 16px
    line-height 20px
    font-weight 500
    +$phone()
        display none

.social
    display flex
    margin-top auto
    &-link
        font-size 24px
        color #A9ACAD
        cursor pointer
        margin-left 16px
        display flex
        +$phone()
            margin 0 8px

</style>
