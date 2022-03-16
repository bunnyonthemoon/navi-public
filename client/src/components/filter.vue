<template lang="pug">

.filter-container
    .mobile-options
        .mobile-options-filters(v-if="is_catalog" @click="mobile_active = true")
            g-icon(name="ui/filter")
            span Фильтры
        .mobile-options-find(v-else @click="load") Показать {{ filter.found }} объект
        .mobile-options-view(v-if="filter.view == 'list'" @click="setView('map')")
            g-icon(name="ui/map")
            span На карте
        .mobile-options-view(v-else-if="filter.view == 'map'" @click="setView('list')")
            g-icon(name="ui/list")
            span Списком


    form.filter(@submit.prevent="load" :class="{ 'mobile-active': mobile_active }")

        .block.bedrooms
            .label Спален
            .rooms
                .room(v-for="(item, index) in bedrooms" :key="index" @click="setBedrooms(item.value)" :class="{ active: filter.bedrooms.indexOf(item.value) != -1 }") {{ item.text }}

        .block.area
            .label Площадь (м²):
            .slider
                .value от 
                    span {{ parseInt(filter.area.values[0]) }}
                .value до 
                    span {{ parseInt(filter.area.values[1]) }}
                v-slider.slider-line(v-model="filter.area.values" :min="filter.area.min" :max="filter.area.max" :tooltips="false" @change="setArea($event)" :lazy="false")

        .block.price
            .label Цена (млн Р):
            .slider
                .value от 
                    span {{ parseInt(filter.price.values[0] / 10**6) }}
                .value до 
                    span {{ parseInt(filter.price.values[1] / 10**6) }}
                v-slider.slider-line(v-model="filter.price.values" :min="filter.price.min" :max="filter.price.max" :tooltips="false" @change="setPrice($event)" :lazy="false")

        .block.type.desktop.tablet
            v-multiselect.select(v-model="filter.class.choosen" placeholder="Класс недвижимости" :options="filter.class.variants" mode="tags" @change="setClass('desktop', $event)")

        .block.type.mobile
            .label Класс недвижимости
            .type-btns
                .type-btn(v-for="variant in filter.class.variants" :key="variant" :class="{ active: filter.class.choosen.indexOf(variant) != -1 }" @click="setClass('mobile', variant)") {{ variant }}

        .block.done.desktop.tablet
            v-multiselect.select(v-model="filter.deadline.choosen" placeholder="Срок сдачи" :options="filter.deadline.variants" mode="tags" @change="setDeadline('desktop', $event)")
        .block.done.mobile
            .label Срок сдачи
            .done-btns
                .done-btn(v-for="date in filter.deadline.variants" :key="date" :class="{ active: filter.deadline.choosen.find(item => item == (date.value ? date.value : date)) }" @click="setDeadline('mobile', date)") {{ date.label ? date.label : date }}

        .block.search
            input(v-model="filter.search" placeholder="Название ЖК, район, метро")
            g-icon(name="ui/search")

        .block.submit.desktop
            button.submit-btn(type="submit") Показать ({{ filter.found }})

        .block.view.desktop
            .view-btn(v-if="filter.view == 'list'" @click="setView('map')")
                g-icon(name="ui/map")
                span На карте
            .view-btn(v-else-if="filter.view == 'map'" @click="setView('list')")
                g-icon(name="ui/list")
                span Списком

        .block.options.mobile
            .options-count Подобрано {{ filter.found }} объекта
            .options-btns
                .cancel(@click="mobile_active = false") Отменить
                button.submit-btn(type="submit") Показать ({{ filter.found }})

</template>
<script>
import vSlider from '@vueform/slider'
import vMultiselect from '@vueform/multiselect'
export default {
    props: {
        is_catalog: Boolean
    },
    data: () => ({
        bedrooms: [
            {
                text: 'Студия',
                value: '0'
            },
            {
                text: '1',
                value: '1'
            },
            {
                text: '2',
                value: '2'
            },
            {
                text: '3',
                value: '3'
            },
            {
                text: '4+',
                value: '4+'
            },
        ],
        done: [
            {
                text: 'Строящиеся',
                value: false
            },
            {
                text: 'Готовые',
                value: true
            },
        ],
        mobile_active: false
    }),
    methods: {
        load() {
            this.mobile_active = false
            if (this.is_catalog)
                this.$emit('load')
            else 
                this.$router.push({ name: 'catalog', query: {...this.$store.getters['catalog/serverOptions']} })
        },
        setBedrooms(value) {
            let index = this.filter.bedrooms.indexOf(value)
            
            if (index == -1)
                this.filter.bedrooms.push(value)
            else this.filter.bedrooms.splice(index, 1)

            // this.load()
        },
        setDone(value) {
            this.filter.done = this.filter.done === value ? null : value

            // this.load()
        },
        setPrice() {
            // this.load()
        },
        setArea() {
            // this.load()
        },
        setDeadline(type, value) {
            if (type == 'desktop') 
                this.filter.deadline.choosen = value
            else {
                if (value.value) value = value.value
                let index = this.filter.deadline.choosen.indexOf(value)
            
                if (index == -1)
                    this.filter.deadline.choosen.push(value)
                else this.filter.deadline.choosen.splice(index, 1)
            }
        },
        setClass(type, value) {
            if (type == 'desktop') 
                this.filter.class.choosen = value
            else {
                let index = this.filter.class.choosen.indexOf(value)
            
                if (index == -1)
                    this.filter.class.choosen.push(value)
                else this.filter.class.choosen.splice(index, 1)
            }
        },
        setView(value) {
            this.filter.view = value
            if (this.is_catalog)
                this.$store.dispatch('catalog/updateRoute')
            else 
                this.$router.push({ name: 'catalog', query: {...this.$store.getters['catalog/serverOptions']} })
        },
        test(a, s) {
            console.log(a, s)
        }
    },
    computed: {
        filter() {
            return this.$store.state.catalog.filter
        }
    },
    components: { vMultiselect, vSlider }
}
</script>
<style src="@vueform/multiselect/themes/default.css"></style>
<style src="@vueform/slider/themes/default.css"></style>
<style lang="stylus" scoped>

.mobile-options
    display none
    +$phone()
        display flex
        padding 20px 16px
        background-color #fff
        justify-content space-between
        &-filters
            $btn('border')
            width 45%
            .icon
                font-size 24px
            .icon + span
                margin-left 10px
        &-find
            $btn('primary')
            width 45%
            padding-left 0
            padding-right 0
        &-view
            $btn('border')
            width 45%
            .icon
                font-size 24px
            .icon + span
                margin-left 10px

.filter
    width $desktop-width
    margin auto
    background-color #fff
    padding 0 20px 20px
    border-radius 20px
    display flex
    // flex-direction column
    flex-wrap wrap
    align-items flex-end
    box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.15)
    &-item
        display flex
        padding 5px
    +$tablet()
        width 100%
        padding 0 "calc(50% - %s / 2) 20px" % $tablet-width
        border-radius 0
        box-shadow none
    +$phone()
        display none
        position fixed
        z-index 20
        top 54px
        left 0
        right 0
        bottom 0
        padding 30px 16px 130px
        overflow-y auto
        flex-direction column
        // width 100%
        align-items stretch
        flex-wrap nowrap
        &.mobile-active
            display flex

.row
    display flex
    align-items flex-end
    margin-top 28px
    position relative
    &:first-child
        margin-top 0
.block
    margin-top 28px
    &.mobile
        display none
    +$phone()
        margin-top 30px
        &.desktop
            display none
        &.mobile
            display flex
        &:first-child
            margin-top 0

.label
    font-size 14px
    line-height 18px
    color $gray
    margin-bottom 10px

.g-btn
    border 1px solid $gray
    border-radius 8px
    font-weight 500
    color $gray

.rooms
    display flex
    margin-right 28px
    +$phone()
        margin-right 0
        // margin-top 0
    .room
        $btn('border')
        margin-right 10px
        border-color $gray2
        width 40px
        height 40px
        padding 0
        &.active
            $btn('secondary')
            padding 0
            width 40px
            height 40px
        &:first-child
            width auto
            padding 0 14px
        &:last-child
            margin-right 0
            


.slider
    width 100%
    height 40px
    padding 0 20px
    position relative
    display flex
    align-items center
    justify-content space-between
    background-color #F4F4F4
    .value
        color $gray
        span
            color $black
            font-weight 500
    &-line
        position absolute
        width 100%
        bottom 0
        left 0
        cursor pointer
        --slider-height 4px
        // --slider-bg $primary
        --slider-connect-bg $primary
        --slider-handle-bg $primary
        --slider-handle-shadow none
        --slider-handle-shadow-active none
    .vue-slider
        position absolute
        width 100%
        bottom 0
        left 0
        right 0
        transform translateY(50%)
        &:deep()
            .vue-slider-dot-handle
                background-color $primary
                box-shadow none
        // padding 0!important


.found
    color $primary
    font-weight 500
    position absolute
    left 50%
    top 50%
    transform translate(-50%, -50%)

.sort
    display inline-flex
    margin-right 19px
    cursor pointer
    .icon
        font-size 18px
        margin-left 9px

.map
    display inline-flex

.type, .done
    flex-shrink 0
    width 270px
    position relative
    height 100%
    &.mobile
        display none
    +$tablet()
        width 350px
    +$phone()
        height auto
        width 100%
        order 3
        flex-wrap wrap
        &.desktop
            display none
        &.mobile
            display flex
            flex-direction column
        &-btns
            display flex
            flex-wrap wrap
            margin-top -10px
        &-btn
            $btn('border')
            margin-right 10px
            border-color $gray2
            height 40px
            margin-top 10px
            &.active
                $btn('secondary')
                font-weight 400
            &:last-child
                margin-right 0


.done
    margin-right 28px
    +$tablet()
        margin-right 0
        margin-left 26px
    +$phone()
        margin-left 0
.select
    width 100%
    --ms-radius 9px
    --ms-dropdown-radius 9px
    box-shadow none
    --ms-border-color $gray2
    --ms-tag-bg $secondary
    // position absolute
    // bottom 0

.search
    width 100%
    width 530px
    height 40px
    // align-self stretch
    position relative
    display flex
    align-items center
    
    +$tablet()
        width 400px
    +$phone()
        width 100%
        order 1
        flex-shrink 0
    input
        position absolute
        width 100%
        height 100%
        top 0
        border 1px solid $gray2
        border-radius 10px
        padding 1px 17px 0
        font-size 14px
        line-height 18px
        &::placeholder
            font-size 14px
            line-height 18px
            color $gray
    .icon
        position absolute
        right 16px
        font-size 24px
        color $gray

.submit
    flex-shrink 0
    margin-left 33px
    margin-right 20px
    &-btn
        $btn('primary')
        height 40px

.view
    flex-shrink 0
    &-btn
        $btn('border')
        height 40px
        border-color $tertiary
        .icon
            font-size 24px

.area, .price
    width 260px
    // flex-shrinks 0
    +$tablet()
        width 196px
    +$phone()
        order 2
        width 100%

.price
    margin-left 24px
    margin-right 28px
    +$tablet()
        margin-right 0
    +$phone()
        margin-left 0

.options
    flex-direction column
    width 100%
    position fixed
    z-index 2
    bottom 0
    width 100%
    left 0
    background-color #fff
    box-shadow: 0px -4px 12px rgba(0, 0, 0, 0.15)
    padding 20px 16px 16px
    margin-top 0
    &-count
        font-weight 500
        color $primary
        text-align center
    &-btns
        display flex
        justify-content space-between
        width 100%
        margin-top 18px
    .cancel
        $btn('border')
        border-color #CCCED0
        color $gray
        width 45%
    .submit-btn
        width 45%

</style>
