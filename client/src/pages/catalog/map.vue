<template lang="pug">

.map-container
    .list
        i-complex(v-for="complex in rendered" :key="complex.id" :complex="complex" :horizontal="true" @click.prevent.stop="opened = complex.id" @mouseover="hover = complex.id" @mouseleave="hover = null")
        .empty(v-if="rendered.length == 0") Результаты не найдены

    GMapMap.map(:center="{lat: 51.093048, lng: 6.842120}" :zoom="15" ref="map" :options="mapOptions" @idle="redraw_complexes")

        GMapCluster.catalog-map-cluster(:zoomOnClick="true" :styles="[{ width: 40, height: 40 }]")

            GMapMarker.catalog-map-marker2(v-for="complex in rendered" :key="complex.id" :position="complex.coordinates" :optimized="false" :label="{ text: `от ${parseInt(complex.min_price / 10**6)} млн`, className: hover === complex.id ? 'catalog-map-marker-active' : 'catalog-map-marker' }" :icon="mapIcon" @click="opened = complex.id")

                GMapInfoWindow.catalog-map-window(:opened="complex.id == opened" :closeclick="false")
                    .catalog-map-window-inner
                        .options
                            g-favorite(:id="complex.id" @click.stop="null")
                            //- .favorite
                            //-     g-icon(name="ui/favorite")
                            .close(@click.stop.prevent="opened = null")
                                g-icon(name="ui/close")
                        .img(:style="{ backgroundImage: `url(${complex.image})` }")
                        .info
                            .name {{ complex.name }}
                            router-link.open(:to="{ name: 'complex', params: { id: complex.key } }" target="_blank") Посмотреть

</template>
<script>
import iComplex from 'components/complex'
export default {
    props: {
        complexes: Array
    },
    async mounted() {
        this.rendered = this.complexes
        const { maps: api } = await this.$gmapApiPromiseLazy()
        const map = await this.$refs.map.$mapPromise
        
        this.api = api
        this.map = map

        await this.fitBounds()
    },
    data: () => ({
        mapOptions: {
            zoomControl: true,
            mapTypeControl: false,
            scaleControl: false,
            streetViewControl: false,
            rotateControl: false,
            gestureHandling: 'greedy',
            styles: [
                {
                    "featureType": "all",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "weight": "2.00"
                        }
                    ]
                },
                {
                    "featureType": "all",
                    "elementType": "geometry.stroke",
                    "stylers": [
                        {
                            "color": "#9c9c9c"
                        }
                    ]
                },
                {
                    "featureType": "all",
                    "elementType": "labels.text",
                    "stylers": [
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "all",
                    "stylers": [
                        {
                            "color": "#f2f2f2"
                        }
                    ]
                },
                {
                    "featureType": "landscape",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "landscape.man_made",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "poi",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "all",
                    "stylers": [
                        {
                            "saturation": -100
                        },
                        {
                            "lightness": 45
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#eeeeee"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#7b7b7b"
                        }
                    ]
                },
                {
                    "featureType": "road",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                },
                {
                    "featureType": "road.highway",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "simplified"
                        }
                    ]
                },
                {
                    "featureType": "road.arterial",
                    "elementType": "labels.icon",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "transit",
                    "elementType": "all",
                    "stylers": [
                        {
                            "visibility": "off"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "all",
                    "stylers": [
                        {
                            "color": "#46bcec"
                        },
                        {
                            "visibility": "on"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "geometry.fill",
                    "stylers": [
                        {
                            "color": "#c8d7d4"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.fill",
                    "stylers": [
                        {
                            "color": "#070707"
                        }
                    ]
                },
                {
                    "featureType": "water",
                    "elementType": "labels.text.stroke",
                    "stylers": [
                        {
                            "color": "#ffffff"
                        }
                    ]
                }
            ]
        },
        mapIcon: {
            url: require('@/assets/icons/ui/empty.svg'),
            scaledSize: {width: 100, height: 40},
            labelOrigin: {x: 50, y: 0}
        },
        clusterOptions: {
            clusterClass: 'catalog-map-cluster'
        },
        api: null,
        map: null,
        opened: null,
        rendered: [],
        hover: null
    }),
    watch: {
        complexes() {
            this.rendered = this.complexes
            this.fitBounds()
        }
    },
    methods: {
        async fitBounds() {
            if (!this.api || !this.map) return

            const bounds = new this.api.LatLngBounds()
            
            for (let complex of this.rendered)
                bounds.extend(new this.api.LatLng(complex.coordinates.lat, complex.coordinates.lng))

            await this.map.fitBounds(bounds)
            if (this.map.getZoom() > 12)
                this.map.setZoom(12)
        },
        redraw_complexes() {
            let bounds = this.map.getBounds()
            console.log('REDRAW')
            this.rendered = this.complexes.filter(complex => {
                let lat = complex.coordinates.lat,
                    lng = complex.coordinates.lng

                return lng > bounds.Qa.h && lng < bounds.Qa.j && lat > bounds.ub.h && lat < bounds.ub.j
            })
        }
    },
    components: { iComplex }
}
</script>
<style lang="stylus" scoped>

.map-container
    padding 20px
    padding-right 0
    position relative
    display flex
    margin-bottom 120px
    height calc(100vh - 80px)
    +$tablet()
        padding 0 0 20px
        height auto
    +$phone()
        padding-bottom 0
        margin-bottom 0
        height calc(100vh - 180px)

.list
    width 372px
    height 100%
    overflow-y auto
    flex-shrink 0
    margin-right 20px
    position relative
    +$tablet()
        display none
    &:deep()
        .complex.horizontal
            width 100%
            margin-top 20px
            &:first-child
                margin-top 0
    .empty
        font-size 24px
        font-weight 500
        text-align center
        padding-top 20px

.map
    width 100%
    height 100%
    // height 800px
    +$tablet()
        height calc(100vh - 300px)
    +$phone()
        height 100%
    &:deep()
        .gm-style-iw-d
            max-height none!important
            overflow hidden
        .gm-style-iw
            padding 0
        .cluster
            background-color $secondary
            box-shadow 1px 3px 5px 0 rgba(#000, .15)
            border-radius 100%
            position absolute
            width 40px!important
            height 40px!important
            img
                display none
            span
                color #fff
                font-family $main-font
                font-weight 500
                font-size 20px
                line-height 40px
        .catalog-map-cluster
            background-color red
            display none
        .catalog-map-marker, .catalog-map-marker-active
            background-color $secondary
            cursor pointer
            font-size 13px!important
            font-weight 500
            padding 3px 10px!important
            border-radius 10px
            color #fff!important
            transform translateY(50%)  scale(1)
            font-family $main-font
            transition transform .2s, background-color .2s
        .catalog-map-marker-active
            transform translateY(50%) scale(1.2)
            background-color lighten(#28709E, 5)
        .catalog-map-window
            width 180px
            font-family $main-font
            position relative
            box-shadow: 4px 4px 8px rgba(0, 0, 0, 0.15)
            .img
                height 100px
                width 100%
                background-size cover
            .name
                font-size 14px
                line-height 18px
            .info
                padding 8px
                display flex
                flex-direction column
            .options
                position absolute
                z-index 10
                top 5px
                right 5px
                display flex
                color #fff
                .g-favorite
                    margin-right 7px
                    font-size 23px
                    display flex
                .close
                    font-size 23px
                    display flex
                    cursor pointer
            .open
                $btn('secondary')
                margin-top 5px
                font-size 14px
                padding 5px 10px
                width auto
                // display inline-flex
                align-self stretch


</style>
