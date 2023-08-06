from rest_framework import (
    serializers,
)

from m3_gar.models import (
    AddhouseTypes,
    AddrObj,
    AddrObjParams,
    AddrObjTypes,
    Apartments,
    ApartmentsParams,
    ApartmentTypes,
    CarplacesParams,
    Houses,
    Steads,
    HousesParams,
    HouseTypes,
    ParamTypes,
    ReestrObjects,
    Rooms,
    RoomsParams,
    RoomTypes,
    SteadsParams,
)
from m3_gar.models.hierarchy import (
    AdmHierarchy,
    Hierarchy,
    MunHierarchy,
)
from m3_rest_gar.consts import (
    CODE_PARAM_TYPES_OFFICIAL,
    GAR_DATE_MAX,
)


class ReestrObjectsSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений об адресном элементе в части его идентификаторов
    """
    class Meta:
        model = ReestrObjects
        fields = '__all__'


class HierarchySerializer(serializers.ModelSerializer):
    """
    Базовый сериализатор сведений по иерархии
    """
    objectid = ReestrObjectsSerializer()
    parentobjid = ReestrObjectsSerializer()
    name_with_parents = serializers.SerializerMethodField()
    has_children = serializers.SerializerMethodField()

    class Meta:
        model = Hierarchy
        fields = '__all__'

    def get_name_with_parents(self, obj):
        result_parts = []
        for item in obj.get_ancestors(include_self=True):
            try:
                addr_obj = AddrObj.objects.get(
                    objectid=item.objectid_id,
                    isactual=True,
                )
                official_type = ParamTypes.objects.filter(code=CODE_PARAM_TYPES_OFFICIAL, isactive=True)
                official_param = None
                if official_type:
                    official_param = AddrObjParams.objects.filter(
                        objectid=item.objectid_id,
                        typeid=official_type.get(),
                    )
            except:
                print('error')
            else:
                type_name = addr_obj.type_full_name
                # Если Респ, то Республика, а если г., то город
                if addr_obj.typename and addr_obj.typename[0].islower():
                    type_name = type_name.lower()

                # Делаем так, чтобы не "область Кировская", а "Кировская область"
                # Впрочем, если есть официальное название, то используем его. 
                # Перестановки остаются на уровне районов, городов и т.д.
                if official_param:
                    for actual_param in official_param:
                        # Может быть два официальных названия: Пермский край и Пермская область. Используем то,
                        # которое используется на данный момент. При этом заранее присваиваем наименование,
                        # чтобы не возникла ошибка, когда в рамках цикла по какой-либо причине условие не выполнится.
                        official_name = actual_param.value
                        if type_name.lower() in actual_param.value.lower():
                            official_name = actual_param.value
                            break

                    addr_obj_name = f'{official_name}'
                elif addr_obj.is_prefix_type:
                    addr_obj_name = f'{type_name} {addr_obj.name}'
                else:
                    addr_obj_name = f'{addr_obj.name} {type_name}'

                result_parts.append(addr_obj_name)

        result = ', '.join(result_parts)

        return result

    def get_has_children(self, obj):
        return obj.has_children


class MunHierarchySerializer(HierarchySerializer):
    """
    Сериализатор сведений по иерархии в муниципальном делении
    """
    class Meta:
        model = MunHierarchy
        fields = '__all__'


class AdmHierarchySerializer(HierarchySerializer):
    """
    Сериализатор сведений по иерархии в административном делении
    """
    class Meta:
        model = AdmHierarchy
        fields = '__all__'


class ParamTypesSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по типу параметра
    """
    class Meta:
        model = ParamTypes
        fields = '__all__'


class ParamListSerializer(serializers.ListSerializer):
    """
    Сериализатор списка сведений о классификаторе параметров адресообразующих
    элементов и объектов недвижимости
    """
    def to_representation(self, data):
        data = data.filter(
            enddate=GAR_DATE_MAX,
        ).select_related(
            'typeid',
        )

        return super().to_representation(data)


class ParamSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений о классификаторе параметров адресообразующих
    элементов и объектов недвижимости
    """
    typeid = ParamTypesSerializer()

    class Meta:
        fields = '__all__'
        list_serializer_class = ParamListSerializer


class AddrObjParamsSerializer(ParamSerializer):

    class Meta(ParamSerializer.Meta):
        model = AddrObjParams


class ApartmentsParamsSerializer(ParamSerializer):

    class Meta(ParamSerializer.Meta):
        model = ApartmentsParams


class CarplacesParamsSerializer(ParamSerializer):

    class Meta(ParamSerializer.Meta):
        model = CarplacesParams


class HousesParamsSerializer(ParamSerializer):

    class Meta(ParamSerializer.Meta):
        model = HousesParams


class RoomsParamsSerializer(ParamSerializer):

    class Meta(ParamSerializer.Meta):
        model = RoomsParams


class SteadsParamsSerializer(ParamSerializer):

    class Meta(ParamSerializer.Meta):
        model = SteadsParams


class AddrObjTypesSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по типам адресных объектов
    """
    class Meta:
        model = AddrObjTypes
        fields = '__all__'


class HierarchicalObjSerializerMixin(
    metaclass=serializers.SerializerMetaclass
):
    """
    Примесь для сериализаторов объектов содержащих сведения об иерархии.
    """
    hierarchy = serializers.SerializerMethodField()

    def get_hierarchy(self, obj):
        data = {}

        for name, model in Hierarchy.get_shortname_map().items():
            hierarchy_instance = model.objects.filter(
                objectid=obj.objectid,
                enddate=GAR_DATE_MAX,
                isactive=True,
            ).select_related(
                'objectid',
                'parentobjid',
            ).first()
            hierarchy_serializer = globals()[f'{model.__name__}Serializer']

            if hierarchy_instance and hierarchy_serializer:
                data[name] = hierarchy_serializer(hierarchy_instance).data

        return data


class AddrObjSerializer(
    HierarchicalObjSerializerMixin,
    serializers.ModelSerializer
):
    """
    Сериализатор сведений классификатора адресообразующих элементов
    """
    params = AddrObjParamsSerializer(many=True)
    type_full_name = serializers.SerializerMethodField()

    # На момент описания моделей AddrObjTypes никак не связывается с AddrObj
    # Существующее поле AddrObj.typename - текстовое представление (ул, пер, г, и т.п.)
    # ??? = AddrObjTypesSerializer()

    class Meta:
        model = AddrObj
        fields = '__all__'

    def get_type_full_name(self, obj):
        return obj.type_full_name.lower()


class HouseTypesSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по типам домов
    """
    class Meta:
        model = HouseTypes
        fields = '__all__'


class AddhouseTypesSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по дополнительным типам домов
    """
    class Meta:
        model = AddhouseTypes
        fields = '__all__'


class HousesSerializer(
    HierarchicalObjSerializerMixin,
    serializers.ModelSerializer
):
    """
    Сериализатор сведений по номерам домов улиц городов и населенных пунктов
    """
    params = HousesParamsSerializer(many=True)
    housetype = HouseTypesSerializer()
    addtype1 = AddhouseTypesSerializer()
    addtype2 = AddhouseTypesSerializer()

    class Meta:
        model = Houses
        fields = '__all__'


class SteadsSerializer(
    HierarchicalObjSerializerMixin,
    serializers.ModelSerializer
):
    """
    Сериализатор сведений по земельным участкам
    """

    params = SteadsParamsSerializer(many=True)

    class Meta:
        model = Steads
        fields = '__all__'


class ApartmentTypesSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по типам помещений
    """
    class Meta:
        model = ApartmentTypes
        fields = '__all__'


class ApartmentsSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по помещениям
    """
    params = ApartmentsParamsSerializer(many=True)
    aparttype = ApartmentTypesSerializer()

    class Meta:
        model = Apartments
        fields = '__all__'


class RoomTypesSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по типам комнат
    """
    class Meta:
        model = RoomTypes
        fields = '__all__'


class RoomsSerializer(serializers.ModelSerializer):
    """
    Сериализатор сведений по комнатам
    """
    params = RoomsParamsSerializer(many=True)
    roomtype = RoomTypesSerializer()

    class Meta:
        model = Rooms
        fields = '__all__'
