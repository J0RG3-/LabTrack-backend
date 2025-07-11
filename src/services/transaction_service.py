from datetime import datetime
from os import getenv
from typing import Dict, List, Optional

from dotenv import load_dotenv
from supabase import create_client
from src.models.transaction_model import TransactionCreate, TransactionOut

load_dotenv()

SUPABASE_URL = getenv("SUPABASE_URL")
SUPABASE_KEY = getenv("SUPABASE_SERVICE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

CAMEL_TO_SNAKE = {
    "compoundId": "compound_id",
    "instanceId": "instance_id",
    "startDate": "timestamp",
    "endDate": "timestamp",
}


def col(name: str) -> str:
    """Convierte el nombre camelCase recibido desde el front a snake_case."""
    return CAMEL_TO_SNAKE.get(name, name)

def register_transaction(tx: TransactionCreate) -> TransactionOut:
    data = tx.model_dump()
    data.setdefault("timestamp", datetime.utcnow().isoformat())

    try:
        resp = supabase.table("transactions").insert(data).execute()
        return TransactionOut(**resp.data[0])
    except Exception as e:
        raise Exception(f"No se pudo registrar la transacción: {e}")


def list_transactions(filters: Optional[Dict] = None) -> List[TransactionOut]:
    if filters is None:
        filters = {}

    query = supabase.table("transactions").select("*")

    if "compoundId" in filters:
        query = query.eq(col("compoundId"), filters["compoundId"])
    if "instanceId" in filters:
        query = query.eq(col("instanceId"), filters["instanceId"])
    if "type" in filters:
        query = query.eq("type", filters["type"])
    if "startDate" in filters:
        query = query.gte(col("startDate"), filters["startDate"])
    if "endDate" in filters:
        query = query.lte(col("endDate"), filters["endDate"])

    sort_field = col(filters.get("_sort", "timestamp"))
    desc_order = filters.get("_order", "desc").lower() == "desc"
    query = query.order(sort_field, desc=desc_order)

    if "_limit" in filters:
        limit = int(filters["_limit"])
        query = query.limit(limit)
    if "_page" in filters and "_limit" in filters:
        offset = (int(filters["_page"]) - 1) * int(filters["_limit"])
        query = query.range(offset, offset + int(filters["_limit"]) - 1)

    try:
        resp = query.execute()
        return [TransactionOut(**item) for item in resp.data or []]
    except Exception as e:
        raise Exception(f"Error al obtener transacciones: {e}")


def get_transactions_by_compound(compound_id: str) -> List[TransactionOut]:
    return list_transactions(
        {"compoundId": compound_id, "_sort": "timestamp", "_order": "desc"}
    )


def get_transactions_by_instance(instance_id: str) -> List[TransactionOut]:
    return list_transactions(
        {"instanceId": instance_id, "_sort": "timestamp", "_order": "desc"}
    )


def update_transaction(tx_id: str, updates: TransactionCreate) -> TransactionOut:
    data = updates.model_dump(exclude_unset=True)
    data["updated_at"] = datetime.utcnow().isoformat()

    try:
        resp = (
            supabase.table("transactions").update(data).eq("id", tx_id).execute()
        )
        if not resp.data:
            raise Exception(f"Transacción {tx_id} no encontrada.")
        return TransactionOut(**resp.data[0])
    except Exception as e:
        raise Exception(f"No se pudo actualizar la transacción {tx_id}: {e}")


def delete_transaction(tx_id: str) -> Dict[str, bool]:
    try:
        supabase.table("transactions").delete().eq("id", tx_id).execute()
        return {"success": True}
    except Exception as e:
        raise Exception(f"No se pudo eliminar la transacción {tx_id}: {e}")


def get_transaction_statistics(filters: Optional[Dict] = None) -> Dict:
    txns = list_transactions(filters)

    stats = {
        "total": len(txns),
        "byType": {},
        "totalQuantityUsed": 0,
        "totalQuantityAdded": 0,
        "dateRange": {"earliest": None, "latest": None},
    }

    for tx in txns:
        stats["byType"][tx.type] = stats["byType"].get(tx.type, 0) + 1

        if tx.type in ("use", "waste"):
            stats["totalQuantityUsed"] += tx.quantity
        elif tx.type == "restock":
            stats["totalQuantityAdded"] += tx.quantity

        ts = datetime.fromisoformat(tx.timestamp)
        if not stats["dateRange"]["earliest"] or ts < datetime.fromisoformat(
            stats["dateRange"]["earliest"]
        ):
            stats["dateRange"]["earliest"] = ts.isoformat()
        if not stats["dateRange"]["latest"] or ts > datetime.fromisoformat(
            stats["dateRange"]["latest"]
        ):
            stats["dateRange"]["latest"] = ts.isoformat()

    return stats
